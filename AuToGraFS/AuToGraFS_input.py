
"""
This code generates the option for running AuToGraFS
Writer Mersad Mostaghimi
mersad.mostaghimi@kit.edu
"""
# import  yaml , os
import yaml
import os
import shutil
from ast import literal_eval

if __name__ == '__main__':
    with open('rendered_WaNo.yml') as file:
        WaNo_file = yaml.full_load(file)

    with open("options", "w") as opt_file:
        opt_file.write(" -c control.txt ")
        opt_file.write(" -p %s/database " % os.getcwd())

        if WaNo_file["Extcontrol"]:
            # tar =tarfile.open(WaNo_file["database"],"r:gz")
            # tar.extractall()
            # tar.close
            shutil.unpack_archive(WaNo_file["database"])
        else:
            os.mkdir("database")
            os.mkdir("database/centers")
            os.mkdir("database/linkers")
            with open("control.txt", "w") as controlfile:
                controlfile.write("topology = %s \n" % WaNo_file["Topology"])
                controlfile.write("center = Center \n")
                os.replace("Center.inp", "database/centers/Center.inp")
                if WaNo_file["Topology"] == "sql":
                    controlfile.write("linker = Linker \n")
                elif WaNo_file["Topology"] == "pcu":
                    if WaNo_file["Pillar linker"]:
                        controlfile.write("linker = Plinker \n")
                        os.replace("Plinker.inp", "database/linkers/Plinker.inp")
                    else:
                        controlfile.write("linker = Linker \n")
                    if WaNo_file["Third linker"]:
                        controlfile.write("Third linker = Tlinker \n")
                        os.replace("Tlinker.inp", "database/linkers/Tlinker.inp")
                    else:
                        controlfile.write("linker = Linker \n")
                    controlfile.write("linker = Linker \n")

                os.replace("Linker.inp", "database/linkers/Linker.inp")

        if WaNo_file["Set supercell"]:
            WaNo_file["supercell"] = literal_eval(WaNo_file["supercell"])[0]
            opt_file.write(" -s %i,%i,%i " % (WaNo_file["supercell"][0],
                                              WaNo_file["supercell"][1],
                                              WaNo_file["supercell"][2]))

        if WaNo_file["leave_ghosts"]:
            opt_file.write(" --leave_ghosts ")

        if WaNo_file["no-leave_ghosts"]:
            opt_file.write(" --no-leave_ghosts ")

        if WaNo_file["OUTPUT EXTN"]:
            opt_file.write(" -e %s " % WaNo_file["OUTPUT_EXTN"])

        if WaNo_file["Output prefix"]:
            opt_file.write(" -o %s " % WaNo_file["output_prefix"])
    exit(0)
