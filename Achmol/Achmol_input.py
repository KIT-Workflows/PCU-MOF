"""
This code generates the option for running Achmol
"""
import yaml  , shutil
#import tarfile 
from ast import literal_eval
if __name__ == '__main__':
    with open('rendered_WaNo.yml') as file:
        WaNo_file = yaml.full_load(file)
    with open("options","w") as opt_file:

        if WaNo_file["INPUT_type"] == "CONTCAR":
            opt_file.write(" -i  CONTCAR " )
        elif WaNo_file["INPUT_type"] == "vasprun.xml":
            shutil.copyfile(WaNo_file["INPUT_FILE"],"vasprun.xml" )
            opt_file.write(" -i  vasprun.xml " )
        elif WaNo_file["INPUT_type"] == "sample.cif":
            shutil.copyfile(WaNo_file["INPUT_FILE"],"sample.cif" )
            opt_file.write(" -i  sample.cif " )
 
        opt_file.write(" -t %s " %WaNo_file["TOPOLOGY"])
        if WaNo_file["Dimer"]:
            opt_file.write(" -d  " )
 
        if WaNo_file["Metal finding"] == "By index":
            opt_file.write(" -m %s "%WaNo_file["Metals indices"])
        elif WaNo_file["Metal finding"] == "Don't remove" :
            opt_file.write(" -m no ")
