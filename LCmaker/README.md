# LCmaker

This **WaNo** performs lcmaker to create the MOF linkers and centers files (*inp* and *xyz*) for running AuToGraFs and automatically generates dummies, in the places, where organic linker should be linked to the metal node. It supports automatic algorithms for dummies selection both for layer and pillar linkers. In an automatic option: carboxyl groups in layer linkers are exchanged by dummies, while for pillar linkers, dummies are positioned on nitrogen atoms.

|Option | Explanation |Example|
| -------------| -------------| -------------|
|linker | A file that contains a linker molecule in a format supported by ASE. | alpha.xyz |
|Input format | The extension (format) of the input file. | xyz |
|Optional | User-defined linker and SBU features, e.g. dummies, shape etc. | - | 
|Dummy | The set of atom indices (based on their indices in "ase gui") to put dummies near them. "None" is used for the automatic algorithm for dummies next to the N or instead of carboxyl groups | 12,5 or None |
|Remove atoms | The set of atom indices (based on their indices in "ase gui") that has to be removed. "None" is used for the automatic algorithm to find carboxyl groups and remove them | 12,5 or None |
|Output | The output name of the linker or SBU | linker |
|SBU | Select secondary building units (SBU) type. | linker or center |
|Shape | Set the shape of SBU from the list. | pcu |
|Xplace | Can be used, if dummies should be replaced with the atoms in the dummy option.| false |
|AuToGraFs | The path to the AuToGraFs directory, where the mol2inp file is located.  | $AuToGraFS_HOME |
|Linker type | For Autografs before version 2.0, which creates inp linkers and centers. | True |

![Semantic description of image](lcmaker.png)
