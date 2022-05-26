import torch
import torch.nn
import kornia
from odak.learn.tools import blur_gaussian

class MultiplaneLoss():
    """
    Loss function for computing loss in multiplanar images. Unlike, previous methods, this loss function accounts for defocused parts of an image.
    """


    def __init__(self, target_image, target_depth, blur_ratio=0.25, target_blur_size=10, number_of_planes=4, weights=[1., 2.1, 0.6, 0.], multiplier=1., scheme='defocus', reduction='mean', cuda=True):
        """
        Parameters
        ----------
        target_image      : torch.tensor
                            Monochrome target image (mxn resolution).
        target_depth      : torch.tensor
                            Monochrome target depth, same resolution as target_image.
        target_blur_size  : int
                            Maximum target blur size.
        blur_ratio        : float
                            Blur ratio, a value between zero and one.
        number_of_planes  : int
                            Number of planes.
        weights           : list
                            Weights of the loss function.
        multiplier        : float
                            Multiplier to multipy with targets.
        scheme            : str
                            The type of the loss, `naive` without defocus or `defocus` with defocus.
        reduction         : str
                            Reduction can either be 'mean', 'none' or 'sum'. For more see: https://pytorch.org/docs/stable/generated/torch.nn.MSELoss.html#torch.nn.MSELoss
        cuda              : bool
                            If set to True, device is cuda. Otherwise CPU.
        """
        self.device           = torch.device("cuda" if cuda else "cpu")
        self.target_image     = target_image.float().to(self.device)
        self.target_depth     = target_depth.float().to(self.device)
        self.target_blur_size = target_blur_size
        self.number_of_planes = number_of_planes
        self.multiplier       = multiplier
        self.weights          = weights
        self.reduction        = reduction
        self.blur_ratio       = blur_ratio
        self.set_targets()
        if scheme == 'defocus':
            self.add_defocus_blur()
        self.loss_function = torch.nn.MSELoss(reduction=self.reduction)


    def get_targets(self):
        """
        Returns
        -------
        targets           : torch.tensor
                            Returns a copy of the targets.
        target_depth      : torch.tensor
                            Returns a copy of the normalized quantized depth map.

        """
        return self.targets.detach().clone(), self.target_depth.detach().clone() / (self.number_of_planes - 1)


    def set_targets(self):
        """
        Internal function for slicing the depth into planes without considering defocus. Users can query the results with get_targets() within the same class.
        """
        self.target_depth = self.target_depth * (self.number_of_planes - 1)
        self.target_depth = torch.round(self.target_depth, decimals=0)
        self.targets      = torch.zeros(
                                        self.number_of_planes,
                                        self.target_image.shape[0],
                                        self.target_image.shape[1],
                                        requires_grad=False
                                       ).to(self.device)
        self.masks        = torch.zeros_like(self.targets).to(self.device)
        for i in range(self.number_of_planes):
            mask_zeros = torch.zeros_like(self.target_image, dtype=torch.int)
            mask_ones = torch.ones_like(self.target_image, dtype=torch.int)
            mask = torch.where(self.target_depth==i, mask_ones, mask_zeros)
            new_target = kornia.filters.unsharp_mask(
                                                     self.target_image.unsqueeze(0).unsqueeze(0),
                                                     (9, 9), (5, 5)
                                                    ) * mask
            self.targets[i] = new_target.squeeze(0).squeeze(0)
            self.masks[i] = mask.detach().clone() 


    def add_defocus_blur(self):
        """
        Internal function for adding defocus blur to the multiplane targets. Users can query the results with get_targets() within the same class.
        """
        targets_cache = self.targets.detach().clone()
        target = torch.sum(targets_cache, axis=0)
        kernel_length = [self.target_blur_size, self.target_blur_size ]
        for i in range(self.number_of_planes):
            sigmas = torch.linspace(start=0,end=self.target_blur_size,steps=self.number_of_planes)
            sigmas = sigmas-i*self.target_blur_size/(self.number_of_planes-1+1e-10)
            defocus = torch.zeros_like(targets_cache[i])
            for j in range(self.number_of_planes):
                nsigma  = [abs(i-j) / self.number_of_planes * self.target_blur_size * self.blur_ratio , abs(i-j) / self.number_of_planes * self.target_blur_size * self.blur_ratio] 
                if i != j and torch.sum(targets_cache[j]) > 0:
                    defocus_plane = blur_gaussian(
                                                  target.detach().clone(),
                                                  kernel_length=kernel_length,
                                                  nsigma=nsigma
                                                 )
                    defocus_plane = defocus_plane * torch.abs(self.masks[j])
                    defocus = defocus + defocus_plane
            self.targets[i] = self.targets[i] + defocus
        self.targets = self.targets.detach().clone() * self.multiplier
    

    def __call__(self, image, target, plane_id=None):
        """
        Calculates the multiplane loss against a given target.
        
        Parameters
        ----------
        image         : torch.tensor
                        Image to compare with a target.
        target        : torch.tensor
                        Target image for comparison.
        plane_id      : int
                        Number of the plane under test.
        
        Returns
        -------
        loss          : torch.tensor
                        Computer loss.
        """
        l2 = self.weights[0] * self.loss_function(image, target)
        if isinstance(plane_id, type(None)):
            mask = self.masks
        mask = self.masks[plane_id]
        l2_mask = self.weights[1] * self.loss_function(image * mask, target * mask)
        l2_cor = self.weights[2] * self.loss_function(image * target, target * target)
        edge_loss = self.weights[3] * self.loss_function(
                                                         kornia.filters.sobel(image.unsqueeze(0).unsqueeze(0)) * mask,
                                                         kornia.filters.sobel(target.unsqueeze(0).unsqueeze(0)) * mask
                                                        )
        loss = l2 + l2_mask + l2_cor + edge_loss
        return loss


    def to(self, device):
        """
        Utilization function for setting the device.
        """
        self.device = device
        return self
