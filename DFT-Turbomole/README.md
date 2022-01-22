# DFT-Turbomole

## Description

This WaNo allows the users to perform pure or hybrid DFT as well was TDDFT calculations using the [TURBOMOLE](https://www.turbomole.org/) code without requiring a deep understanding of TURBOMOLE's functionalities and input files. The user can choose between single point calculations, structure optimisations and frequency calculations (using TURBOMOLE’s ```aoforce```). The mandatory input of this WaNo consists of either a tar file of an old Turbomole calculation or an initial structure which can provided in xyz, coord or Gaussian input format where the latter allows the user to specify the charge and multiplicity of the molecule directly via the input file.

## Server setup

The code is based on python and the necessary virtual environment on the server is provided by Simstack. In addition, a configuration file called ```turbomole.config``` needs to be provided in ```$NANOMATCH/$NANOVER/configs``` on the server where the environment variable $NANOVER can be adjusted in the xml file. The config file is responsible for setting up the TURBOMOLE environment on the cluster which can be done by loading a corresponding module or by defining all necessary environment variables and adjusting ```$PATH``` and ```$LD_LIBRARY_PATH``` as described in the TURBOMOLE manual.

## Required input

The only required input is an initial structure which can be provided either as a structure file or through a results tar file from a previous calculation. 

## WaNo Settings

- **Follow-up calculation**  
If chosen, a results archive of a previous calculation can be used to provide an initial structure (and optionally also an initial guess for the wavefunction).

- **Title**  
An string can be given as a title for the calculation (optional).

- **Molecular structure**
This is the only mandatory input (see above), and the structure can either be given as an xyz, coord or Gaussian input file. Alternatively, the ```coord``` file of a previous calculation can be read if 'Follow-up calculation' is selected.

- **Basis set**  
Several commonly used basis-sets can be chosen with 'def2-SVP' as the default options. 

- **Initial guess**  
The default setting is for a neutral closed-shell molecule. If the chosen values for charge and multiplicity are not possible for the given structure, the multiplicity will automatically be adjusted, i.e. reduced by one (until a minimum of 1). If ‘Gaussian input’ is chosen as the input file format, the user can select to the charge and multiplicity defined in the input file, but no check for consistency is possible (the WaNo will fail for impossible combinations). In case of a follow-up calculation, it is also possible to use the old orbitals as initial guess.

- **DFT options**  
In this box, the parameters of DFT calcution are defined, as for example the functional as well as (optionally) a type of dispersion correction and the use of COSMO model for description of solvation effects.

- **Type of calculation**  
The user can choose between ground and excited state calculations. Please be aware that frequency calculations for excited states are currently not possible, and that the WaNo will skip the frequency calculation if ‘Excited state calculation’ is chosen.

## Output

The output of this WaNo consists of the final structure in xyz format (which is equivalent to the initial structure for single point calculations), a yml file (```turbomole_results.yml```) containing the total energy, the HOMO-LUMO gap as well as the energies for electronic or vibrational transitions) and an archive file with all relevant output files for further analysis or follow-up calculations.
