#!/usr/bin/env python3

"""
Script that uses a rendered WaNo for input to calculate Lambda, EA, and IP.
"""

import yaml
from yaml import CLoader

if __name__ == "__main__":
    with open("rendered_wano.yml", "r") as WaNoin:
        WaNo = yaml.load(WaNoin, Loader=CLoader)
    engines = []
    for engine in WaNo["Tabs"]["Engines"]["DFT Engines"]:
        # Reformats engine output from NewQP rendered WaNo
        engine_name = engine["Engine"]
        name = engine["Name"]
        engine_settings = engine["%s Settings" % engine_name]
        engines.append({"Name": name,
                        "DFT Engine": engine_name,
                        "Settings": engine_settings})
    tmp = WaNo["Tabs"]["General"]["General Settings"]
    molecule = {"Path": tmp["Morphology"],
                "Charge": 0,
                "Multiplicity": 0
                }
    settings = {"Molecule": molecule,
                "Engines": engines,
                "LambdaEAIP": WaNo["Tabs"]["LambdaEAIP"]
                }
    with open("LambdaEAIP_settings.yml", "w") as WaNoout:
        yaml.dump(settings, WaNoout, default_flow_style=False)
