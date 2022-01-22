import pymatgen
from pymatgen.core.structure import Structure, Lattice
from pymatgen.io.vasp import Incar, Poscar, Potcar, Kpoints
from ast import literal_eval
import os, sys, re, yaml

#kpoints = Kpoints.gamma_automatic([3, 3, 3], [0, 0, 0])
#kpoints = Kpoints.monkhorst_automatic([3, 3, 3], [0, 0, 0])
#kpoints = Kpoints.automatic(50)
#poscar = Poscar.from_file("POSCAR")
#kpoints = Kpoints.automatic_density(poscar.structure, 500, True)

if __name__ == '__main__':

    if os.path.isfile('KPOINTS'):
        print("KPOINTS already loaded")
        exit
    else:
        with open('rendered_WaNo.yml') as file:
                WaNo_file = yaml.full_load(file)

        Rk = WaNo_file["TABS"]["KPOINTS"]["Kpoints_length"]
        Monkhorst = WaNo_file["TABS"]["KPOINTS"]["Kpoints_Monkhorst"]

        if  Rk:
            Rk_val = (WaNo_file["TABS"]["KPOINTS"]["Rk_length"])
            kpoints = Kpoints.automatic(Rk_val)
        elif Monkhorst:
            mat_n = literal_eval(WaNo_file["TABS"]["KPOINTS"]["Monkhorst"])
            n = [mat_n[0][0], mat_n[0][1], mat_n[0][2]]
            n_shift = [mat_n[1][0], mat_n[1][1], mat_n[1][2]]
            kpoints = Kpoints.monkhorst_automatic(n, n_shift)
            # kpoints = Kpoints.gamma_automatic(n, n_shift)
        else:
            None

        kpoints.write_file('KPOINTS')
        print("KPOINTS successfully created")