# SuperCeller 

This **WaNo** performs SuperCeller that makes an *xyz* Cartesian supercell file of the molecules from Achmol (atoms of each linker are grouped (indices) to the particular linker), based on the lattice parameters taken from another structure file with a lattice parameter (for example, CONTCAR or POSCAR format).
SuperCeller takes the position of the atoms from an *xyz* file and repeats it based on a multiplication of an integer number with the cell parameters of the file that provides unit-cell parameters. Its output is used to perform the calculation in *QuantumPatch3* WaNo.

![Semantic description of image](superceller.png)
