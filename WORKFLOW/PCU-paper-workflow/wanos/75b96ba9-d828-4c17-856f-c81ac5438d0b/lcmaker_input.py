"""
This code generates the option for running AuToGraFs
"""
import yaml  , shutil
if __name__ == '__main__':
    with open('rendered_WaNo.yml') as file:
        WaNo_file = yaml.full_load(file)
    shutil.copyfile(WaNo_file["Input file"],"%s.%s" %(WaNo_file["Output"],WaNo_file["Input format"]))
    with open("options","w") as opt_file:
        opt_file.write(f""" -i {WaNo_file["Output"]}.{WaNo_file["Input format"]}""")

        if WaNo_file["Optional"]:
            if eval(WaNo_file["Dummy"]):
                opt_file.write(" -d %s "%WaNo_file["Dummy"])
 
            opt_file.write(" -p %s " %WaNo_file["Shape"])
 
            opt_file.write(" -s %s " %WaNo_file["SBU"])
            
            if eval(WaNo_file["Remove atoms"]):
                opt_file.write(f""" -r %s """%WaNo_file["Remove atoms"])
 
            if WaNo_file["AuToGraFs"]:
                opt_file.write(" -a %s " %WaNo_file["AuToGraFs PATH"])
 
            if WaNo_file["Xplace"]:
                opt_file.write(" -x ")
 
            if WaNo_file["Linker_type"] == "xyz":
                opt_file.write(" -t ")

 
