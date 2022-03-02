#!/usr/bin/env python3

"""
Script that uses WaNo input to write QuantumPatch input.
"""

import yaml, copy
from yaml import CLoader


class QuantumPatchWaNoError(Exception):
    pass


if __name__ == "__main__":
    with open("rendered_wano.yml", "r") as wanoin:
        wano = yaml.load(wanoin, Loader=CLoader)
    with open("qp_settings_template.yml", "r") as qpngin:
        cfg = yaml.load(qpngin, Loader=CLoader)  # Script will modify this and re-write it
    # Shorthands
    wano_shells = wano["Tabs"]["Shells"]
    wano_core = wano_shells["Core Shell"]
    wano_general = wano["Tabs"]["General"]["General Settings"]
    wano_postproc = wano["Tabs"]["Post processing"]
    qp_run = wano_general["QuantumPatch Type"]
    max_iter = wano_core["Screened Iterations"]
    # Indirection arrays to translate settings from WaNo expression to input
    qp_type = {"Polarized": "uncharged_equilibration",
               "Polaron/Exciton": "charged_equilibration",
               "Matrix EAIP": "matrix_eaip",
               "Excitonic Preprocessing": "excitonic_preprocessing",
               "Absorption": "absorption"  }
    shelltype = {"dynamic": "scf",
                 "static": "static"}
    # settings_ng "QuantumPatch" Category
    cfg["QuantumPatch"]["type"] = qp_type[qp_run]
    cfg["QuantumPatch"]["number_of_equilibration_steps"] = max_iter
    cfg["QuantumPatch"]["calculateJs"] = wano_general["Calculate Js"]
    cfg["QuantumPatch"]["charge_damping"] = wano_general["Charge Damping"]
    cfg["Analysis"]["HigherOrder"] = {}
    cfg["Analysis"]["HigherOrder"]["ExtraJs"] = int(wano_general["Higher Order Js"])
    cfg["Analysis"]["homo_lumo_generator"] = {}
    cfg["Analysis"]["homo_lumo_generator"]["enabled"] = wano_postproc["Predict site energy distribution"]
    cfg["Analysis"]["homo_lumo_generator"]["periodic_copies"] = [int(wano_postproc["Site energy prediction settings"]["Periodic copies"]["x"]), int(wano_postproc["Site energy prediction settings"]["Periodic copies"]["y"]), int(wano_postproc["Site energy prediction settings"]["Periodic copies"]["z"])]
    cfg["Analysis"]["homo_lumo_generator"]["non_PBC_morphology"] = wano_postproc["Site energy prediction settings"]["non PBC Structure"]
    cfg["Analysis"]["homo_lumo_generator"]["swap_x_z_axis"] = wano_postproc["Site energy prediction settings"]["z Rotation"]
    cfg["Analysis"]["homo_lumo_generator"]["coulomb_cutoff"] = wano_postproc["Site energy prediction settings"]["ESP average options"]["Coulomb cutoff"]
    cfg["Analysis"]["homo_lumo_generator"]["esp_avrg_options"] = {}
    cfg["Analysis"]["homo_lumo_generator"]["esp_avrg_options"]["z-extend"] =  wano_postproc["Site energy prediction settings"]["ESP average options"]["Include copies for evironment in z-direction"]
    if wano_postproc["Site energy prediction settings"]["ESP average options"]["Distance binning"] == True:
        this_mode = "by_distance"
    else:
        this_mode = "no_binning_by_distance"
    cfg["Analysis"]["homo_lumo_generator"]["esp_avrg_options"]["mode"] = this_mode
    cfg["Analysis"]["homo_lumo_generator"]["esp_avrg_options"]["bins_per_nm"] = float(wano_postproc["Site energy prediction settings"]["ESP average options"]["Bins per nanometer"])
    # settings_ng "DFTEngine" Category
    cfg["DFTEngine"]["user"] = dict()
    for engine in wano["Tabs"]["Engines"]["DFT Engines"]:
        # Reformats engine output from NewQP rendered WaNo
        engine_name = engine["Engine"]
        name = engine["Name"]
        settings = engine["%s Settings" % engine_name]
        if engine_name == "Turbomole" or engine_name == "Psi4":
            entry = {
                "engine": engine_name,
                "basis": settings["Basis"],
                "functional": settings["Functional"],
                "threads": settings["Threads"],
                "memory": settings["Memory (MB)"],
                "dispersion": settings["D3(BJ) Dispersion Correction"],
                "charge_model": settings["Partial Charge Method"],
            }
        elif engine_name == "DFTB+":
            entry = {
                "engine": "DFTBplus",
                "threads": settings["Threads"],
                "memory": settings["Memory (MB)"],
                "dispersion": settings["D3(BJ) Dispersion Correction"],
                "charge_model": settings["Partial Charge Method"],
            }
        elif engine_name == "XTBEngine":
            entry = {
                "engine": engine_name,
                "threads": settings["Threads"],
                "memory": settings["Memory (MB)"],
                "charge_model": settings["Partial Charge Method"],
            }
        else:
            raise QuantumPatchWaNoError("Unknown DFT engine %s" % engine_name)
        if engine_name == "Turbomole":
            entry["scf_convergence"] = settings["SCF Convergence"]
        if engine["Fallback"]:
            entry["fallback"] = engine["Fallback Engine"]
        cfg["DFTEngine"]["user"][name] = entry
    # settings_ng "System" Category
    cfg["System"]["Core"] = dict()
    if wano_core["Inner Part Method"] == "Number of Molecules":
        cfg["System"]["Core"]["type"] = "number"
        cfg["System"]["Core"]["number"] = wano_core["Number of Molecules"]
    elif wano_core["Inner Part Method"] == "Number of Molecules of each Type":
        cfg["System"]["Core"]["type"] = "number_by_type"
        cfg["System"]["Core"]["number"] = wano_core["Number of Molecules"]
    elif wano_core["Inner Part Method"] == "Inner Box Cutoff":
        cfg["System"]["Core"]["type"] = "distance"
        cfg["System"]["Core"]["distance"] = {
            "cutoff_x": wano_core["Inner Box Cutoff"]["Cutoff x direction"],
            "cutoff_y": wano_core["Inner Box Cutoff"]["Cutoff y direction"],
            "cutoff_z": wano_core["Inner Box Cutoff"]["Cutoff z direction"]
        }
    elif wano_core["Inner Part Method"] == "Number of Random Pairs":
        cfg["System"]["Core"]["type"] = "random_molstate_pairs"
        cfg["System"]["Core"]["number"] = wano_core["Number of Molecules"]
    elif wano_core["Inner Part Method"] == "Number of Random Crosspairs":
        cfg["System"]["Core"]["type"] = "random_molstate_crosspairs"
        cfg["System"]["Core"]["number"] = wano_core["Number of Molecules"]
    elif wano_core["Inner Part Method"] == "list of Molecule IDs":
        cfg["System"]["Core"]["type"] = "list"
        cfg["System"]["Core"]["list"] = wano_core["list of Molecule IDs"]
    by_iter = dict()  # Inserts engine_by_iter section
    if wano_core["Different Engine on Last Iteration"]:
        by_iter["LastUncharged"] = wano_core["Last Iteration Engine"]
        by_iter["LastCharged"] = wano_core["Last Iteration Engine"]
        by_iter["Dimer"] = wano_core["Last Iteration Engine"]
    cfg["System"]["Core"]["engine_by_iter"] = by_iter
    cfg["System"]["Core"]["engine"] = wano_core["Used Engine"]
    cfg["System"]["Core"]["default_molstates"] = wano_core["Default Molecular States"]
    cfg["System"]["Core"]["GeometricalOptimizationSteps"] = []
    i = 0
    cfg["System"]["Shells"] = dict()
    for shell in wano_shells["Outer Shells"]:
        cfg["System"]["Shells"][str(i)] = {
            "cutoff": shell["Shell"]["Cutoff Radius"],
            "type": shelltype[shell["Shell"]["Shelltype"]],
            "engine": shell["Shell"]["Used Engine"]
        }
        by_iter = dict()  # Inserts engine_by_iter section
        if shell["Shell"]["Different Engine on Last Iteration"]:
            by_iter["LastUncharged"] = shell["Shell"]["Last Iteration Engine"]
            by_iter["LastCharged"] = shell["Shell"]["Last Iteration Engine"]
            by_iter["Dimer"] = shell["Shell"]["Last Iteration Engine"]
        cfg["System"]["Shells"][str(i)]["engine_by_iter"] = by_iter
        i += 1
    cfg["System"]["MolStates"] = dict()
    i = 0
    for molstate in wano["Tabs"]["General"]["Molecular States"]:
        cfg["System"]["MolStates"][str(i)] = {
            "charge": molstate["State"]["Charge"],
            "multiplicity": molstate["State"]["Multiplicity"],
            "excited_state_of_interest": molstate["State"]["Excited State of Interest"],
            "roots": molstate["State"]["Roots"]
        }
        i += 1
    # Analysis section options
    if wano_general["QuantumPatch Type"] == "Matrix EAIP":
        if wano_general["Include in-matrix Lambda Calculation"]:
            cfg["Analysis"]["MatrixEAIP"]["do_lambda"] = True
        else:
            cfg["Analysis"]["MatrixEAIP"]["do_lambda"] = False


    # copy core shell to last iter shell in case of exciton disorder
    do_exciton_disorder = wano_postproc["Compute excion disorder in last iteration"]
    if do_exciton_disorder == True:
        core_engine_name = cfg["System"]["Core"]["engine"]
        core_engine_dict = cfg["DFTEngine"]["user"][core_engine_name]
        dft_engine = core_engine_dict["engine"]
        # assert that Turbomole is used in the core shell for exciton disorder
        assert dft_engine == "Turbomole", "Exciton disorder only works with Turbomole core engine. Disable exciton disorder in the post processing tab or chose a Turbomole core engine"
        # copy core engine
        new_engine_dict = copy.deepcopy(core_engine_dict)
        # add new options
        new_engine_dict["excited_state_of_interest"] = 1
        new_engine_dict["gs_partial_charges_for_excitation"] = True
        # add new engine to engines dict
        cfg["DFTEngine"]["user"][core_engine_name + " LI"] = new_engine_dict
        # get engine by iter dict of core shell
        core_ebi_dict = cfg["System"]["Core"]["engine_by_iter"]
        if "LastUncharged" in core_ebi_dict.keys():
            print("Last iter is already defined for core engine. Exciton disorder will most likely fail")
        else:
             cfg["System"]["Core"]["engine_by_iter"]["LastUncharged"] = core_engine_name + " LI"


    # Write modified settings file to disk.
    with open("settings_ng.yml", "w") as qpngout:
        yaml.dump(cfg, qpngout, default_flow_style=False)


