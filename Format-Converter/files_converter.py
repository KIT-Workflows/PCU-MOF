import yaml
import numpy as np
from ase import Atoms
from ase.lattice.cubic import SimpleCubic
#from ase.io import read, write
from ase import io

# vasp, cif, xyz, pdb

def check_xyz_cell(struct):
    cell = struct.get_cell()
    if cell.any() == 0.0:
        dist = struct.get_all_distances()
        latt_cubic = np.max(dist)*1.25 # same than VESTA  
        lattice = SimpleCubic(symbol='Cu',latticeconstant=latt_cubic)              
        cell = latt_cubic
    struct.cell = lattice.get_cell()
    print(struct.get_cell())
    return struct

with open('rendered_wano.yml') as file:
    WaNo_file = yaml.full_load(file)

input_file = WaNo_file["Input-File"]
input_format = WaNo_file["Input-Format"]
output_name = WaNo_file["Output-File-Name"]
output_format = WaNo_file["Output-Format"]

struct = io.read(input_file, format = input_format)
if input_format == "xyz":
    struct = check_xyz_cell(struct)

struct.write(output_name + "." + output_format)

#struct.write('test.pdb')
# cell = struct.get_cell()
# # pos = struct.get_positions()
# # dist = struct.get_all_distances()
# # print(np.max(dist)*1.25) # 25%
# check_xyz_cell(struct)
# # struct.get_cell()