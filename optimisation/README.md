# Description

This folder contains our optimisation method for multiplane Computer-Generated Holography (CGH). 
Please clone the entire repository and navigate to the `optimisation` folder in your favourite terminal application to run this code. 
Note that this folder requires the other folders in the same repository.

```
git clone git@github.com:complight/realistic_defocus.git
cd realistic_defocus/optimisation
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

# (1) Running the optimisation
Once you have the requirements successfully installed, you are ready to run the optimisation code. 
As a first check, please make sure to run the optimisation with default settings.

```
cd realistic_defocus/optimisation
python3 main.py
```

If all goes well, you should have seen a progress bar of this optimisation. A new directory named `output` must have been created. 
Within this new directory, you can find an optimised hologram, the same hologram with a grating term added, reconstructions of the same hologram at various planes and target images for each plane.

# (2) Configuring the optimisation to your taste
Assuming that you have successfully optimised your first multiplane hologram, we can now consider configuring the optimisation for your case.

Note that there is a `settings` directory within the `optimisation` folder. 
This specific directory contains a `sample.txt` for configuring the optimisation.
For example, `sample.txt` looks like this:

```
{


    "general"     : {
                     "cuda"                  : 1,
                     "iterations"            : 60,
                     "propagation type"      : "Bandlimited Angular Spectrum",
                     "output directory"      : "./output",
                     "optimisation mode"     : "Stochastic Gradient Descent",
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

