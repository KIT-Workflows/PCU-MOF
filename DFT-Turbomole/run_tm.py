import os, sys, yaml, shutil

import turbomole_functions as tm
import ase.io

from pymatgen.io import xyz
from pymatgen.io.gaussian import GaussianInput

################################################################
###                                                          ###
### prerequisite files: rendered_wano.yml, initial_structure ###
###                                                          ###
################################################################

def get_settings_from_rendered_wano():
    global wano_file

    disp_dict={'None':'off','D2':'old','D3':'on','D3-BJ':'bj','D4':'d4'}

    settings=dict()
    
    settings['title'] = wano_file['Title']
    settings['follow-up'] = wano_file['Follow-up calculation']
    settings['use old struct'] = wano_file['Molecular structure']['Use old structure']
    settings['structure file type'] = wano_file['Molecular structure']['Structure file type']
    settings['int coord'] = wano_file['Molecular structure']['Internal coordinates']
    settings['old basis'] = wano_file['Basis set']['Use basis set from previous calculation']
    settings['basis set'] = wano_file['Basis set']['Basis set type']
    settings['use old mos'] = wano_file['Initial guess']['Use old orbitals']
    settings['charge from file'] = wano_file['Initial guess']['G1']['Use charge and multiplicity from input file']
    settings['charge'] = wano_file['Initial guess']['G1']['Charge']
    settings['multiplicity'] = wano_file['Initial guess']['G1']['Multiplicity']
    settings['old dft options'] = wano_file['DFT options']['Use parameters from previous calculation']
    settings['scf iter'] = 60
    settings['max scf iter'] = wano_file['DFT options']['G1']['Adv options']['Max SCF iterations']
    settings['use ri'] = wano_file['DFT options']['G1']['Adv options']['Use RI']
    settings['ricore'] = wano_file['DFT options']['G1']['Adv options']['Memory for RI']
    settings['functional'] = wano_file['DFT options']['G1']['Functional']
    settings['grid size'] = wano_file['DFT options']['G1']['Adv options']['Integration grid']
    settings['disp'] = disp_dict[wano_file['DFT options']['G1']['vdW correction']]
    settings['cosmo'] = wano_file['DFT options']['G1']['COSMO calculation']
    settings['epsilon'] = wano_file['DFT options']['G1']['Rel permittivity']
    settings['opt'] = wano_file['Type of calculation']['Structure optimisation']
    settings['opt cyc'] = 50
    settings['max opt cyc'] = wano_file['Type of calculation']['Max optimization cycles']
    settings['freq'] = wano_file['Type of calculation']['Frequency calculation']
    settings['tddft'] = wano_file['Type of calculation']['Excited state calculation']
    settings['exc state type'] = wano_file['Type of calculation']['TDDFT options']['Type of excited states']
    settings['num exc states'] = int(wano_file['Type of calculation']['TDDFT options']['Number of excited states'])
    settings['opt exc state'] = int(wano_file['Type of calculation']['TDDFT options']['Optimised state'])

    return settings

def sanitize_multiplicity(multi,n_el):

    multi_new=multi
    multi_min=n_el%2+1

    if multi < 1:
        print('Attention: a multiplicity of %i is not possible.'%(multi))

    elif n_el%2 and multi%2: 
        print('Attention: a multiplicity of %i is not possible for an odd number of electrons.'%(multi))
        multi_new-=1
    elif not n_el%2 and not multi%2: 
        print('Attention: a multiplicity of %i is not possible for an even number of electrons.'%(multi))
        multi_new-=1

    if multi_new < multi_min: multi_new=multi_min
    if multi != multi_new:
        print('The multiplicity was set to %i by default'%(multi_new))
    
    return multi_new

if __name__ == '__main__':
    
    with open('rendered_wano.yml') as infile:
        wano_file = yaml.full_load(infile)

    coord_file = 'coord_0'
    settings = get_settings_from_rendered_wano()

    if settings['follow-up']: 
        os.mkdir('old_results')
        os.system('tar -xf old_calc.tar.xz -C old_results')

        if settings['use old struct']: 
            shutil.copy('old_results/coord', coord_file)

        with open('old_results/settings.yml') as infile:
            old_settings = yaml.full_load(infile)

        settings['title'] = old_settings['title']

        if settings['old basis']:
            settings['basis set'] = old_settings['basis set']

        if settings['use old mos']:
            settings['multiplicity'] = old_settings['multiplicity']

        if settings['old dft options']:
            for key in ['max scf iter', 'use ri', 'ricore', 'functional', 'grid size', 'disp', 'cosmo', 'epsilon']:
                settings[key] = old_settings[key]
    
    if not os.path.isfile(coord_file):
        if settings['structure file type'] == 'Turbomole coord':
            os.rename('initial_structure',coord_file)

        else:
            if settings['structure file type'] == 'Gaussian input':
                ginp = GaussianInput.from_file('initial_structure')
                xyz.XYZ(ginp.molecule).write_file('initial_structure')

            os.system('x2t initial_structure > %s'%(coord_file))

    if not settings['use old mos']:
        if settings['charge from file'] and settings['structure file type'] == 'Gaussian input':
            settings['charge'], settings['multiplicity'] = ginp.charge, ginp.spin_multiplicity

        else:
            n_el = sum(ase.io.read(coord_file).numbers)-settings['charge']
            settings['multiplicity'] = sanitize_multiplicity(settings['multiplicity'],n_el)

    with open('settings.yml','w') as outfile:
        yaml.dump(settings, outfile)

    tm.inputprep('define',tm.make_define_str(settings,coord_file))

    if settings['follow-up']:
        os.system('rm -rf old_results')

    if settings['cosmo']:
        if settings['follow-up']:
            if old_settings['cosmo']:
                tm.inputprep('cosmoprep','u\n%f\n\n\n\n\n\n\n\n\n\n\n*\n\n\n'%(settings['epsilon']))
            else: tm.inputprep('cosmoprep','%f\n\n\n\n\n\n\n\n\n\n\nr all b\n*\n\n\n'%(settings['epsilon']))
        else: tm.inputprep('cosmoprep','%f\n\n\n\n\n\n\n\n\n\n\nr all b\n*\n\n\n'%(settings['epsilon']))

    elif settings['follow-up'] and old_settings['cosmo']:
       for datagroup in ['cosmo','cosmo_atoms','cosmo_out']: os.system('kdg %s'%(datagroup))

    if settings['tddft'] and settings['opt']:
        if not settings['cosmo']: os.system('adg exopt %i'%settings['opt exc state'])
        else:
            print('Excited state optimisations with COSMO not yet implemented in Turbomole\'s egrad - A single-point calculation is performed instead')
            settings['opt']=False

    tm.single_point_calc(settings)

    if settings['opt']:
        tm.jobex(settings)

    if settings['freq']:
        if settings['tddft']: 
            print('Frequency calculations for excited states not yet implemented')
            exit(0)
        else: tm.aoforce()

    results_dict = {}
    results_dict['title'] = settings['title']
    results_dict['energy_unit'] = 'Hartree'

    with open('energy') as infile: results_dict['energy'] = float(infile.readlines()[-2].split()[1])
    with open('eiger.out') as infile: results_dict['homo-lumo gap'] = float(infile.readlines()[14].split()[2])

    if settings['tddft']:
        results_dict['exc_type'] = settings['exc state type']
        excitations = []

        with open('exspectrum') as infile:
            exc_lines = infile.readlines()[-settings['num exc states']:]

        for exc_line in exc_lines:
            exc_dict = {'exc energy': float(exc_line.split()[2]), 'osc. strength': float(exc_line.split()[-2])}
            excitations.append(exc_dict)
        results_dict['electronic excitations'] = excitations

    elif settings['freq']:
        vib_spectrum = []

        with open('aoforce.out') as infile:
            ao_lines = infile.readlines()

        for i in range(len(ao_lines)):
            if 'frequency  ' in ao_lines[i]:
                frequencies = ao_lines[i].split()[1:]
                intensities = ao_lines[i+6].split()[2:]
                for j in range(len(frequencies)):
                    if 'i' in frequencies[j]:
                        freq = -float(frequencies[j].replace('i',''))

                    else:
                        freq = float(frequencies[j])

                    freq_dict = {'frequency': freq, 'intensity': float(intensities[j])}
                    vib_spectrum.append(freq_dict)

            if 'zero point' in ao_lines[i]:
                results_dict['ZPE'] = float(ao_lines[i].split()[6])

        results_dict['vibrational frequencies'] = vib_spectrum

    with open('turbomole_results.yml','w') as outfile:
        yaml.dump(results_dict,outfile)

    output_files = ['alpha','auxbasis','basis','beta','control','coord','energy','forceapprox','gradient','hessapprox','mos','optinfo','settings.yml','sing_a','trip_a','unrs_a'] # implement symmetry: irrep names in [sing,trip,unrs]_irrep
    for filename in output_files:
        if not os.path.isfile(filename):
            output_files.remove(filename)

    os.system('tar -cf results.tar.xz %s'%(' '.join(output_files)))
    os.system('t2x coord > final_structure.xyz')
