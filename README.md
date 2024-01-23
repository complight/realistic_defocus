# 13 DEC 2023 --> Moving on forward consider using [multi-color hologram codebase](https://github.com/complight/multi_color)

## Realistic Defocus Blur for Multiplane Computer-Generated Holography
[Koray Kavaklı](https://www.linkedin.com/in/koray-kavakli-75949241/),
[Yuta Itoh](https://www.ar.c.titech.ac.jp/people/yuta-itoh),
[Hakan Ürey](https://mems.ku.edu.tr/),
and [Kaan Akşit](https://kaanaksit.com)

<img src='./teaser.png' width=800>

[Website](https://complightlab.com/publications/realistic_defocus_cgh/), [Manuscript](https://arxiv.org/abs/2205.07030), [Video]()

# Description
This work focuses on improving the visual image quality of computer-generated holography. 
It achieves that by mitigating fringe effects found in the state of the art computer-generated holography.

This work contains three important components:

* [Our Multiplane Loss Function and targeting scheme](losses)
* [Multiplane Optimisation using our loss function and modified Stochastic Gradient descent](optimization)

Note that each part has its own `README.md` to explain its usage.
However, our loss function does not have such a `README.md`, therefore please consult the `docstrings` [inside the code](losses/__init__.py#L12-L33) to understand workings of our loss function. 
If you need support beyond these `README.md` files, please do not hesitate to reach us using `issues` section.

# Citation
If you find this repository useful for your research, please consider citing our work using the below `BibTeX entry`.
```
@misc{kavakli2022realisticdefocus,
    doi = {10.48550/ARXIV.2205.07030},
    url = {https://arxiv.org/abs/2205.07030},
    author = {Kavaklı, Koray and Itoh, Yuta and Urey, Hakan and Akşit, Kaan},
    keywords = {Computer Vision and Pattern Recognition (cs.CV), Graphics (cs.GR), FOS: Computer and information sciences, FOS: Computer and information sciences, I.3.3},
    title = {Realistic Defocus Blur for Multiplane Computer-Generated Holography},
    publisher = {arXiv},
    year = {2022},
    copyright = {Creative Commons Attribution Non Commercial No Derivatives 4.0 International}
}
```

# Getting started with the code

This folder contains our optimization method for multiplane Computer-Generated Holography (CGH). 
Please clone the entire repository and navigate to the `optimization` folder in your favourite terminal application to run this code. 
Note that this folder requires the other folders in the same repository.

```
git clone git@github.com:complight/realistic_defocus.git
cd realistic_defocus
```

Note that this code is tested with an NVIDIA Geforce RTX 2080 on Ubuntu 21. 
We do not guarantee that the codebase can work in other operating systems (e.g., Windows, Android, Mac or any other Unix derivatives that we didn't test).

# (0) Install the required dependencies
In the root directory, you will find `requirements.txt`. 
This specific file can help you to install the required packages using `pip`:

```
cd realistic_defocus
pip3 install -r requirements.txt
```

Note that we often update `odak`, if this `requirements.txt` fails, please use the below syntax to install odak:

```
pip3 install git+https://github.com/kaanaksit/odak
```

Also make sure to pull all the large files using Large-File-Format support:

```
git lfs pull
```


# (1) Running the optimization
Once you have the requirements successfully installed, you are ready to run the optimization code. 
As a first check, please make sure to run the optimization with default settings.

```
python3 main.py
```

If all goes well, you should have seen a progress bar of this optimization. A new directory named `output` must have been created. 
Within this new directory, you can find an optimized hologram, the same hologram with a grating term added, reconstructions of the same hologram at various planes and target images for each plane.


# (2) Configuring the optimization to your taste
Assuming that you have successfully optimized your first multiplane hologram, we can now consider configuring the optimization for your case.

Note that there is a `settings` directory. 
This specific directory contains a `sample.txt` for configuring the optimization.
For example, `sample.txt` looks like this:

```
{


    "general"     : {
                     "cuda"                  : 1,
                     "iterations"            : 60,
                     "propagation type"      : "Bandlimited Angular Spectrum",
                     "output directory"      : "./output",
                     "optimization mode"     : "Stochastic Gradient Descent",
                     "learning rate"         : 0.04,
                     "hologram number"       : 1
                    },


    "target"      : {
                     "image filename"        : "../dataset/test/images/couch_rgb.png",
                     "depth filename"        : "../dataset/test/depths/couch_rgb.png",
                     "scheme"                : "defocus",
                     "color channel"         : 0,
                     "defocus blur size"     : 10,
                     "blur ratio"            : 0.25,
                     "number of planes"      : 6,
                     "mask limits"           : [0.0, 1.0, 0.0, 1.0], 
                     "multiplier"            : 1.0,
                     "weights"               : [1.0, 1.0, 1.0, 0.0]
                    },


    "image"       : {
                     "location"              : 0.0,
                     "delta"                 : 0.001,
                     "zero mode distance"    : 0.3
                    },  


    "slm"         : {
                     "model"                 : "Holoeye Pluto 1.3.3",
                     "pixel pitch"           : 0.000008,
                     "resolution"            : [1080, 1920]
                    },    


    "beam"        : {
                     "wavelength"            : 0.000000515
                    }


}
```

All of these variables are named in a self-explanatory fashion. 
If you are looking into finding more sample images, consider visiting our [images repository](https://github.com/complight/images).


# Acknowledgements
The authors would like to thank reviewers for their valuable feedback. We also thank Erdem Ulusoy and Güneş Aydındoğan for discussions in the early phases of the project; Tim Weyrich and Makoto Yamada for dedicating GPU resources in various experimentation phases; David Walton for their feedback on the manuscript; Kaan Akşit is supported by the Royal Society's RGS\R2\212229 - Research Grants 2021 Round 2 in building the hardware prototype.

