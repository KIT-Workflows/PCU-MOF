"""
This code generates the option for running AuToGraFS
"""
#import  yaml , os
import  yaml , tarfile , os,shutil
from ast import literal_eval

if __name__ == '__main__':
    with open('rendered_wano.yml') as file:
        WaNo_file = yaml.full_load(file)
    if float(WaNo_file["Zdistance"]) :
        with open("%s.%s" %(WaNo_file["output_prefix"],WaNo_file["OUTPUT_EXTN"] ) ,"r") as mainfile:
            lines = mainfile.readlines()
            line4 = lines[4].split()
            line4[2] ="%f \n" %WaNo_file["Zdistance"]
            line4 = "   ".join(line4)
            lines[4] = line4
        with open("%s.%s"%(WaNo_file["output_prefix"],WaNo_file["OUTPUT_EXTN"]) ,"w") as mainfile:
            for i in lines:
                mainfile.write(i)

