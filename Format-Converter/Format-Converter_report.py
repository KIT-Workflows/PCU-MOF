import yaml

if __name__ == '__main__':

    with open("rendered_WaNo.yml") as file:
        WaNo_file = yaml.full_load(file)

    with open("output_dict.yml",'w') as out:
        yaml.dump(WaNo_file, out,default_flow_style=False)
    
