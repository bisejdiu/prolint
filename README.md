# ProLint
A python package for the automated analysis and visualization of **Pro**tein-**L**ipid **int**eractions.


ProLint is a lightweight python library that has four core objectives:
* Powerful and customizable analysis of protein-lipid contacts
* Allow for quick and easy insight into simulation data
* Increase data sharing and accessibility
* Automation of protein-lipid contact generation


To get familiar with ProLint please read the <a href="https://prolint.readthedocs.io" target="_blank">documentation</a>.
## Installation

If you have `conda` installed, then you can install ProLint's dependencies by typing: 

```sh
# create new environment
conda create --name prolint python=3.7
# install dependencies
conda install -c conda-forge numpy==1.15.4 pandas==0.24.0 mdtraj==1.9.2 scipy pyyaml colorcet bokeh==1.4.0 networkx nglview==2.7.7 matplotlib jupyterlab
```

After that, then you clone this directory and install it, using: 

```sh
git clone https://github.com/bisejdiu/prolint.git
cd prolint
python setup.py install
```

## Getting Started

Please follow the instructions provided in the <a href="https://prolint.readthedocs.io" target="_blank">documentation</a> to get started. Note that, to use the visualization interface of ProLint, 
you should use JupyterLab. At the top of your notebook file, make sure to call the `output_notebook` function: 

```python
from bokeh.io import output_notebook
output_notebook()
```

Additionally, if you want to use the `show_contact_projection` function, make sure that your installation of `nglview` is working properly. 
Follow the instruction provided by <a href="https://github.com/nglviewer/nglview" target="_blank">there</a> to ensure your installation is running correclty.

## Notes
This library has been tested with the Martini model. It should work with atomistic simulations quite well, however testing so far has been very limited. 
During the following weeks we'll continue updating the library as well as adding & improving its functionality. 
