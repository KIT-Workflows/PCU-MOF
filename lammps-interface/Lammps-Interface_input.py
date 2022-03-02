"""
This code generates the option for running Achmol
"""
import yaml  , shutil
#import tarfile 
from ast import literal_eval
if __name__ == '__main__':
    with open('rendered_wano.yml') as file:
        WaNo_file = yaml.full_load(file)
    with open("options","w") as opt_file:
        opt_file.write(" -ff %s "%WaNo_file["Force Field options"]["FORCE FIELD"])
        opt_file.write(" --dreid-bond-type %s "% WaNo_file["Force Field options"]["dreid bond type"])
        opt_file.write(" --cutoff %f "% WaNo_file["Simulation options"]["cutoff"])
        opt_file.write(" --tolerance  %f "%WaNo_file["Parameter options"]["tolerance"])
        opt_file.write(" --neighbour-size %i "%WaNo_file["Parameter options"]["neighbour size"])
        opt_file.write(" --iter-count %i "%WaNo_file["Parameter options"]["iter count"])
        opt_file.write(" --max-deviation %f "%WaNo_file["Parameter options"]["max deviation"])
        opt_file.write(" --temperature %f "%WaNo_file["Parameter options"]["temperature"])
        opt_file.write(" --pressure %f "%WaNo_file["Parameter options"]["pressure"])
        opt_file.write(" --production-steps %i "%WaNo_file["Parameter options"]["production steps"])
        opt_file.write(" --equilibration-steps %i"%WaNo_file["Parameter options"]["equilibration steps"])
 

        if  WaNo_file["Force Field options"]["molecule ff"] != "same firce field":
            opt_file.write(" --molecule-ff %s "% WaNo_file["Force Field options"]["molecule ff"])
        if WaNo_file["Force Field options"]["h bonding"]:
            opt_file.write(" --h-bonding " )
        if WaNo_file["Force Field options"]["fix metal"]:
            opt_file.write(" --fix-metal " )
        if WaNo_file["Simulation options"]["minimize"]:
            opt_file.write(" --minimize " )
        if WaNo_file["Simulation options"]["bulk moduli"]:
            opt_file.write(" --bulk-moduli " )
        if WaNo_file["Simulation options"]["npt"]:
            opt_file.write(" --npt ")
        if WaNo_file["Simulation options"]["nvt"]:
            opt_file.write(" --nvt ")
        if WaNo_file["Simulation options"]["REPLICATION"]:
            WaNo_file["Simulation options"]["replication"]=literal_eval(WaNo_file["Simulation options"]["replication"])[0]
            opt_file.write(" --replication %i,%i,%i " %(WaNo_file["Simulation options"]["replication"][0],WaNo_file["Simulation options"]["replication"][1],WaNo_file["Simulation options"]["replication"][2]) )
        if WaNo_file["Simulation options"]["orthogonalize"]:
            opt_file.write(" --orthogonalize ")
        if WaNo_file["Simulation options"]["randomize velocities"]:
            opt_file.write(" --randomize-velocities ")
        if WaNo_file["Simulation options"]["dcd"]:
            opt_file.write(" --dcd %i " %WaNo_file["Simulation options"]["dcd"])
        if WaNo_file["Simulation options"]["xyz"]:
            opt_file.write(" --xyz %i" %WaNo_file["Simulation options"]["xyz"])
        if WaNo_file["Simulation options"]["lammpstrj"]:
            opt_file.write(" --lammpstrj %i "%WaNo_file["Simulation options"]["lammpstrj"])
        if WaNo_file["Simulation options"]["restart"]:
            opt_file.write(" --restart ")
        if WaNo_file["outputcif"]:
            opt_file.write(" -o ")
        if WaNo_file["outputpdb"]:
            opt_file.write(" -p")
        if WaNo_file["outputraspa"]:
            opt_file.write(" -or ")

        opt_file.write(" lammps.cif ")
