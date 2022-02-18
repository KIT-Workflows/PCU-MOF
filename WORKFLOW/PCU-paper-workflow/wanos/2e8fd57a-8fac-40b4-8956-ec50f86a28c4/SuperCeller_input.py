"""
This code generates the option for running AuToGraFs
"""
import yaml  , shutil
if __name__ == '__main__':
    with open('rendered_wano.yml') as file:
        WaNo_file = yaml.full_load(file)
    with open("options","w") as opt_file:
        opt_file.write(" -x %s " %WaNo_file["XYZ_file"])
        opt_file.write(" -l %s " %WaNo_file["Lattice_file"])
        opt_file.write(" -s %i,%i,%i " %(WaNo_file["Xrepeat"],WaNo_file["Yrepeat"],WaNo_file["Zrepeat"]))

   
