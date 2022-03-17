# PCU-MOF Workflow  [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5893325.svg)](https://doi.org/10.5281/zenodo.5893325)

This repository provides the WaNos used in the PCU-MOF Workflow. This workflow is built with the [Simstack](https://www.simstack.de/) framework automates the construction, optimization, and prediction of electronic properties of the PCU topology of metal-organic frameworks. The PCU-MOF workflow consists of three central parts: (1) **MOF Builder**, (2) **MOF Optimizer** and (3) **MOF Analyzer**. 

**MOF Builder** consists of the general WaNo *MOF-input*, where a user specifies linker molecules, metal node type and desired topology, *DFT-Turbomole*, where
optimization of input linkers is done using TURBOMOLE software, *LCmaker* and *AuToGraFS* used to build periodic MOF model. 

**MOF Optimizer** includes WaNo *GULP* for the pre-optimization of MOFs with the force field potentials, *DFT-VASP* for MOF optimization using quantum mechanical approach and *Format-Converter* designed to convert different file formats between software. 

**MOF Analyzer** is assigned to calculate different properties of MOF based on both (a) DFT optimized structures (right branch) or (b) sampled MOF structures during molecular dynamics (MD) simulations using LAMMPS (left branch).

Figure below displays the PCU-MOF workflow as designed in the [Simstack](https://www.simstack.de/) client.
![Semantic description of image](workflow.png)

Description of the PCU-MOF workflow and the demonstration of several use-cases are available [here](https://www.frontiersin.org/articles/10.3389/fmats.2022.840644/full):
>M. Mostaghimi, C. R. C. Rêgo, R. Haldar, C. Wöll, W. Wenzel, M. Kozlowska, *Automated virtual design of organic semiconductors based on metal-organic frameworks*, **Front. Mater.**, 2022, 9: 840644.

## Client installation and WaNos

To get this workflow up running: 
 1. Download the [Simstack](https://www.simstack.de/) client and install it on your local machine by following the steps detailed in the [Simstack documentation](https://simstack.readthedocs.io/en/latest/installation/index.html). 
 3. Copy the WaNos from this repository to your local WaNo Simstack directory.
 4. WaNo to perform Quantum Patch can be accessed from [Nanomatch](https://www.nanomatch.de/virtual-lab/virtual-design-tools/quantumpatch/). 
 5. The functionality of WaNos and implemented setup is available in the respective WaNo documentation.

### Running the workflow
After configuring SimStack and copying WaNos, PCU-MOF workflow can be used either on HPC resources provided by AG Wenzel or on the user specific HPC. WaNos are portable and do not depend on HPC architecture. To fulfill requirements of the second case, please follow installation instruction below. Consider also to adapt WaNos to concrete modules available on your HPC and configure both SimStack client and server before running the workflow.

If you want to use HPC resources of AG Wenzel (with already installed all necessary modules), please contact us via mariana.kozlowska@kit.edu and wolfgang.wenzel@kit.edu for an access. After copying **WaNos** from this repository into WaNos directory inside SimStack and/or **workflow** into the SimStack workflow directory, you can access WaNos and/or workflow directly via SimStack client. If you use **PCU-MOF workflow**, it is enough to upload user-defined *xyz* files of MOF linkers inside the workflow and specify the user-selected setup inside WaNos to run the workflow. You can also drag-and-drop **WaNos** in order to create your own workflow (keep in mind correct input-output file selection between WaNos). If the same setup should be used for the calculation of MOF library, it is enough just to specify *xyz* files in a workflow and click the *Run* button in SimStack. No further modifications are needed.

If you have access to the AG Wenzel HPC, copy the `WORKFLOW/PCU-paper-workflow` in the workflow directory of your SimStack. After loading the SimStack, the workflow can be loaded and used straightly.

### Software installation
The best method for installing the software is installing [ANACONDA](https://docs.anaconda.com/anaconda/install/index.html) with the following libraries:

```
ase                       3.22.0
numpy                     1.21.2
scikit-learn              0.24.1
scipy                     1.6.2
os
time 
optparse
logging
```
We installed the anaconda3 and created a py2 and installed the python 2 on it. In the Module directory, you can find the module file for lua module for the MOFsofts and anaconda. The paths of installation for them in the module file are:
 
```
Anaconda:/shared/software/anaconda3/
MOFsofts:/shared/software/chem/MOFsofts
```

If you just copied MOFsofts without module environment, export the following paths:

```
export PATH=/shared/software/chem/MOFsofts/bin:$PATH
export PATH=/shared/software/chem/MOFsofts/AuToGraFS:$PATH
AuToGraFS_HOME=/shared/software/chem/MOFsofts/AuToGraFS
```

Also for running lcmaker we need python2 that can run AuToGraFS. [Here](https://docs.anaconda.com/anaconda/user-guide/tasks/switch-environment/) is a document that explain the installation of python2 environment on anaconda3:
Create a Python 2 environment named py2, install Python 2.7:

```
conda create --name py2 python=2.7
```

Now you have two environments with which to work. You can install packages and run programs as desired in either one.

Activate and use the Python 2 environment.

Windows:

```
activate py2
```

macOS, Linux:

```
conda activate py2
```

After activation of py2 environment, the library for AuToGraFS must be installed:

```
ase, scipy, numpy<1.15.0
```

There is a module for anaconda for HPCs in the modules directory. The WaNos xml files should be edited according to the place of the related software. 

If you are on HPC, make sure that you have access to openbable whenever you want to run the Achmol.
If it is not available, you need to install OpenBabel (http://openbabel.org/wiki/Main_Page):

```
openbabel > 3.0.0
libxml2
swig
Eigen > 2
```
#### AuToGraFS
We used a costomized version of AuToGraFS that is available in AuToGraFS directory. It is based on the python 2 and call the mofgen.py file to run. to install it, copy the dirextory on your system and export the path in your shell. for bash :

```
export PATH=PATH_TO_AuToGraFS_DIR:$PATH
```

Caution:
As mentioned above, these codes work with openbabel >3.0.0. We test it by compiling openbabel from the source code by the below explanation.
You need the openbabel, which is installed or compiled with -DPYTHON_BINDINGS=ON and  -DRUN_SWIG=ON . To this, you first need to install swing. If you are using Ubuntu or Mint Linux, you can use the below command.

        sudo apt install swig libxml2-dev libxml2 libeigen3-dev 

Download the openbabel from http://openbabel.org/wiki/Category:
Installation
After unzipping it, you can compile it with the below command.

```
 cd TO_OPENBABEL_DIR
 mkdir builder
 cd builder
 cmake .. -DPYTHON_BINDINGS=ON and  -DRUN_SWIG=ON -DCMAKE_INSTALL_PREFIX=/opt/obabel/3.1.1
 make
 make install
```

After installing openbabel in the /opt/obabel/3.1.1, you should introduce it to your bash and also your python. For this, add the below lines to your bash and source it again.

```
export PATH=/opt/obabel/3.1.1/bin:$PATH
export LD_LIBRARY_PATH=/opt/obabel/3.1.1/lib:$LD_LIBRARY_PATH
export INCLUDE=/opt/obabel/3.1.1/include:$INCLUDE
export  PYTHONPATH=/opt/obabel/3.1.1/lib:$PYTHONPATH
```

CAUTION:
Edit all WaNos xml files in the way that passes the required software (anaconda, openbable, AuToGraFS).
For the MOFsofts software, please communicate with Mersad.Mostaghimi@kit.edu.

### Cite us
If you are using PCU-MOF workflow and/or WaNos available in this repository, developed for the MOF design: *LCmaker, AuToGraFS, GULP, lammps-interface,
LAMMPS, Achmol, SuperCeller*, [cite us](https://www.frontiersin.org/articles/10.3389/fmats.2022.840644/full):
>M. Mostaghimi, C. R. C. Rêgo, R. Haldar, C. Wöll, W. Wenzel, M. Kozlowska, *Automated virtual design of organic semiconductors based on metal-organic frameworks*, **Front. Mater.**, 2022, 9: 840644.


If you are interested in further WaNos development for your specific case, contact us via mariana.kozlowska@kit.edu and wolfgang.wenzel@kit.edu

## License & copyright
© M. Mostaghimi, C. R. C. Rêgo, W. Wenzel, M. Kozlowska
Licensed under the [GNU GENERAL PUBLIC LICENSE](LICENSE).
