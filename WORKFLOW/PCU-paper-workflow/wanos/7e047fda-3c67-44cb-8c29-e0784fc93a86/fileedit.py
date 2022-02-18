import yaml
if __name__ == '__main__':
    with open('rendered_wano.yml') as file:
        WaNo_file = yaml.full_load(file)
    if WaNo_file["Fix_cell"]:
        with open("data.lammps","r") as datain:
            lines = datain.readlines()

            Masses=False
            for line in lines:
                if line.startswith("Masses"):
                    Masses=True
                elif line.startswith("Bond"):
                    Masses =False
                if Masses:
                        for metal in ["Li","Be","Na","Mg","Al","K","Ca","Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn","Ga","Rb","Sr","Y","Zr","Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd","In","Sn","Cs","Ba","La","Ce","Prm","Nd","Pm","Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm","Yb","Lu","Hf","Ta","W","Re","Os","Ir","Pt","Au","Hg","Tl","Pb","Bi","Po","Fr","Ra","Ac","Th","Pam","U","Np","Pu","Am","Cm","Bk","Cf","Es","Fm","Md","No","Lr","Rfum","Db","Sg","Bh","Hs","Mt","Dsm","Rg","Cn","Nh","Fl","Mc","Lv"]:
                            if metal in line:
                                metalindex=line.split()[0]


        with open("in.lammps","r") as infile:
            lines = infile.readlines()
            for inx,line in enumerate(lines):
                if line.startswith("#### END Atom Groupings ####"):
                    fixion = "group           metal     type %s\n#### END Atom Groupings ####\nfix 4 metal recenter INIT INIT INIT shift all\n"%metalindex

                    lines.insert(inx,fixion)
                    break

            with open("in.lammps","w") as infile:
                for line in lines:
                    infile.write(line)

