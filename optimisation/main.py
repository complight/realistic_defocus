import sys
import torch
import argparse
from tqdm import tqdm
from odak.learn.wave import linear_grating, calculate_phase
from odak.learn.tools import load_image, save_image
from odak.tools import load_dictionary, check_directory
from odak import np

sys.path.append('../')
from optimisation import multiplane_hologram_optimiser
from losses import MultiplaneLoss

__title__ = 'Realistic Defocus Blur for Multiplane Holography'

def main():
    settings_filename='./settings/sample.txt'
    parser = argparse.ArgumentParser(description=__title__)
    parser.add_argument(
                        '--settings',
                        type=argparse.FileType('r'),
                        help='Filename for the settings file. Default is {}'.format(settings_filename)
                       )
    parser.add_argument(
                        '--colour',
                        type=int,
                        help='Colour channel. Default is as described by the settings file.'
                       )
    args = parser.parse_args()
    if type(args.settings) != type(None):
        settings_filename = str(args.settings.name)
    settings = load_dictionary(settings_filename)
    if type(args.colour) != type(None):
        settings["target"]["color channel"] = args.colour
    check_directory(settings["general"]["output directory"])
    ch = settings["target"]["color channel"]
    target_image = load_image(settings["target"]["image filename"])[:,:,ch]/255.

    target_depth = 1. - load_image(settings["target"]["depth filename"])/255.
    device = torch.device(settings["general"]["device"])
    loss_function = MultiplaneLoss(
                                   target_image=target_image,
                                   target_depth=target_depth,
                                   target_blur_size=settings["target"]["defocus blur size"],
                                   number_of_planes=settings["target"]["number of planes"],
                                   multiplier=settings["target"]["multiplier"],
                                   blur_ratio=settings["target"]["blur ratio"],
                                   weights=settings["target"]["weights"],
                                   scheme=settings["target"]["scheme"],
                                   device=device
                                  )
    targets, depth = loss_function.get_targets()
    for hologram_id in range(settings["general"]["hologram number"]):
        optimiser = multiplane_hologram_optimiser(
                                                  wavelength=settings["beam"]["wavelength"],
                                                  image_location=settings["image"]["location"],
                                                  image_spacing=settings["image"]["delta"],
                                                  slm_pixel_pitch=settings["slm"]["pixel pitch"],
                                                  slm_resolution=settings["slm"]["resolution"],
                                                  targets=targets,
                                                  propagation_type=settings["general"]["propagation type"],
                                                  number_of_iterations=settings["general"]["iterations"],
                                                  learning_rate=settings["general"]["learning rate"],
                                                  number_of_planes=settings["target"]["number of planes"],
                                                  mask_limits=settings["target"]["mask limits"],
                                                  zero_mode_distance=settings["image"]["zero mode distance"],
                                                  optimisation_mode=settings["general"]["optimisation mode"],
                                                  loss_function=loss_function,
                                                  device=device
                                                 )
        phase, reconstructions = optimiser.optimise()
        save(settings, device, phase, reconstructions, targets, depth, hologram_id)


def save(settings, device, phase, reconstructions, targets, depth, hologram_id):
    for plane_id in range(settings["target"]["number of planes"]):
        save_image(
                   settings["general"]["output directory"] + "/target_{:04}.png".format(plane_id), 
                   targets[plane_id], cmin=0, cmax=1.)
    save_image(
               settings["general"]["output directory"] + '/depth.png',
               depth,
               cmin=0.,
               cmax=1.
              ) 
    checker_complex = linear_grating(
                                     settings["slm"]["resolution"][0],
                                     settings["slm"]["resolution"][1],
                                     add = np.pi,
                                     axis='y'
                                    ).to(device)
    checker = calculate_phase(checker_complex)
    phase_grating = phase + checker
    phase_normalized = ((phase % (2 * np.pi)) / (2 * np.pi)) * 255
    save_image(settings["general"]["output directory"]+"/phase_{:04}.png".format(hologram_id), phase_normalized)
    phase_grating = ((phase_grating%(2*np.pi))/(2*np.pi))*255
    save_image(settings["general"]["output directory"]+"/phase_grating_{:04}.png".format(hologram_id), phase_grating)
    if hologram_id == 0:
        k = settings["target"]["number of planes"]
        t = tqdm(range(k),leave=False)
        for plane_id in t:
            save_image(
                       settings["general"]["output directory"]+"/recon_{:04}.png".format(plane_id), 
                       reconstructions[plane_id], cmin=0, cmax=1.)


if "__main__" == "__main__":
    sys.exit(main())
