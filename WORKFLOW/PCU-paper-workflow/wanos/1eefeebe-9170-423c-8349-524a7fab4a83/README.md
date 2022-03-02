# Achmol
This WaNo performs **Achmol** (Assembler of Chemical Molecules) for the extraction of molecules and/or molecular clusters from periodic MOF structures, obtained in VASP, in XYZ format used further in, e.g. *QuantumPatch3* WaNo. It creates both *xyz* and *cml* files. Achmol accepts CONTCAR, vasprun.xml or other ASE-supported file formats with a periodic MOF structure. It extracts the structure, separates linkers by removing metal atoms, finds the nearest linkers based on the bonds and saturates the cutted linkers.

| Option | Explanation | Example | 
|--------------------|---------------|-----------------|
|INPUT_type | Type of input file that is the output of a converged periodic DFT optimization. | CONTCAR  | 
|INPUT_FILE | Output file of DFT optimization (according to data selected in INPUT_type). | CONTCAR  |
|Metal finding | Select the way the metal atoms are found and removed. `Automatic`: finds all metal atoms and remove them. `By index`: user-defined indices of metals (based on the index of atoms in ASE GUI representation). `Dont remove`: nothing is removed | Automatic  | 
|Metals indices | Set the index of at least one metal atom in a MOF | 7,10 |
|TOPOLOGY | Set the topology of target MOF | PCU or SQL |
|Dimer | Additional option to post-process DFT calculations made with the supercell, e.g. 1x1x2. This option was developed for other MOF topologies, e.g. SQL, not studied here. | False |

![Semantic description of image](achmol.png)
