import sys
import os
import torch
import argparse
import odak
from tqdm import tqdm


__title__ = 'Realistic Defocus Blur for Multiplane Holography'


def main():
    settings_filename='./settings/holoeye.txt'
    parser = argparse.ArgumentParser(description=__title__)
    parser.add_argument(
                        '--settings',
                        type=argparse.FileType('r'),
                        help='Filename for the settings file. Default is {}'.format(settings_filename)
                       )
    parser.add_argument(
                        '--color',
                        type=int,
                        help='Color channel. Default is as described by the settings file.'
                       )
    args = parser.parse_args()
    if type(args.settings) != type(None):
        settings_filename = str(args.settings.name)
    settings = odak.tools.load_dictionary(settings_filename)
    if type(args.color) != type(None):
        settings["target"]["color channel"] = args.colour
    odak.tools.check_directory(settings["general"]["output directory"])
    ch = settings["target"]["color channel"]
    target_image = odak.learn.tools.load_image(settings["target"]["image filename"], normalizeby = 255.)[: , :, ch]
    target_depth = 1. - odak.learn.tools.load_image(settings["target"]["depth filename"], normalizeby = 255.)
    if len(target_depth.shape) > 2:
        target_depth = target_depth[:, :, 1]
    device = torch.device(settings["general"]["device"])
    loss_function = odak.learn.wave.multiplane_loss(
                                                    target_image = target_image.unsqueeze(0),
                                                    target_depth = target_depth,
                                                    target_blur_size = settings["target"]["defocus blur size"],
                                                    number_of_planes = settings["target"]["number of planes"],
                                                    multiplier = settings["target"]["multiplier"],
                                                    blur_ratio = settings["target"]["blur ratio"],
                                                    weights = settings["target"]["weights"],
                                                    scheme = settings["target"]["scheme"],
                                                    device = device
                                                   )
    targets, focus_target, depth = loss_function.get_targets()
    for hologram_id in range(settings["general"]["hologram number"]):
        optimizer = odak.learn.wave.multiplane_hologram_optimizer(
                                                                  wavelength = settings["beam"]["wavelength"],
                                                                  image_location = settings["image"]["location"],
                                                                  image_spacing = settings["image"]["delta"],
                                                                  slm_pixel_pitch = settings["slm"]["pixel pitch"],
                                                                  slm_resolution = settings["slm"]["resolution"],
                                                                  targets = targets,
                                                                  propagation_type = settings["general"]["propagation type"],
                                                                  number_of_iterations = settings["general"]["iterations"],
                                                                  learning_rate = settings["general"]["learning rate"],
                                                                  number_of_planes = settings["target"]["number of planes"],
                                                                  mask_limits = settings["target"]["mask limits"],
                                                                  zero_mode_distance = settings["image"]["zero mode distance"],
                                                                  loss_function = loss_function,
                                                                  device = device
                                                                 )
        phase, _, reconstructions = optimizer.optimize()
        save(settings, device, phase, reconstructions, targets, focus_target.squeeze(0), depth, hologram_id)


def save(settings, device, phase, reconstructions, targets, focus_target, depth, hologram_id):
    torch.no_grad()
    for plane_id in range(settings["target"]["number of planes"]):
        odak.learn.tools.save_image(
                                    settings["general"]["output directory"] + "/target_{:04}.png".format(plane_id), 
                                    targets[plane_id], cmin = 0, cmax = 1.)
    odak.learn.tools.save_image(
                                settings["general"]["output directory"] + "/target.png",
                                focus_target, cmin = 0., cmax= 1.)
    odak.learn.tools.save_image(
                                settings["general"]["output directory"] + '/depth.png',
                                depth,
                                cmin = 0.,
                                cmax = 1.
                               ) 
    checker_complex = odak.learn.wave.linear_grating(
                                                     settings["slm"]["resolution"][0],
                                                     settings["slm"]["resolution"][1],
                                                     add = odak.pi,
                                                     axis='y'
                                                    ).to(device)
    checker = odak.learn.wave.calculate_phase(checker_complex)
    phase_grating = phase + checker
    phase_normalized = ((phase % (2 * odak.pi)) / (2 * odak.pi)) * 255
    odak.learn.tools.save_image(settings["general"]["output directory"]+"/phase_{:04}.png".format(hologram_id), phase_normalized)
    phase_grating = ((phase_grating % (2 * odak.pi)) / (2 * odak.pi)) * 255
    odak.learn.tools.save_image(settings["general"]["output directory"]+"/phase_grating_{:04}.png".format(hologram_id), phase_grating)
    if hologram_id == 0:
        k = settings["target"]["number of planes"]
        t = tqdm(range(k),leave=False)
        for plane_id in t:
            odak.learn.tools.save_image(
                                        settings["general"]["output directory"]+"/recon_{:04}.png".format(plane_id), 
                                        reconstructions[plane_id], cmin = 0, cmax = 1.)
    data = {
            "targets" : focus_target,
            "depth" : depth,
            "phases" : phase_normalized / 255.,
            "settings" : settings
           }
    odak.learn.tools.save_torch_tensor('{}/data.pt'.format(settings["general"]["output directory"]), data)
    print('Outputs stored at ' + os.path.expanduser(settings["general"]["output directory"]))


if __name__ == "__main__":
    sys.exit(main())
