"""
This code provides the predefined center (SBU) in Woell WaNo
"""
import yaml  , shutil, sys
if __name__ == '__main__':
    with open('rendered_wano.yml') as file:
        WaNo_file = yaml.full_load(file)
    if not WaNo_file["User SBU"]:
        shutil.copyfile(sys.argv[1]+WaNo_file["Available SBUs"],"Center.inp")


 
