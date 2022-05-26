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
* [Multiplane Optimisation using our loss function and modified Stochastic Gradient descent](optimisation)

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

# Acknowledgements
The authors would like to thank reviewers for their valuable feedback. We also thank Erdem Ulusoy and Güneş Aydındoğan for discussions in the early phases of the project; Tim Weyrich and Makoto Yamada for dedicating GPU resources in various experimentation phases; David Walton for their feedback on the manuscript; Kaan Akşit is supported by the Royal Society's RGS\R2\212229 - Research Grants 2021 Round 2 in building the hardware prototype.

