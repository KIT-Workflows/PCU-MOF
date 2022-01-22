import os,sys,yaml

import turbomole_functions as tm
import ase.io

#######################################################################
###                                                                 ###
### prerequisite files: rendered_WaNo.yml, initial_structure.xyz (coord_0) ###
###                                                                 ###
#######################################################################

def get_settings_from_rendered_WaNo():

    disp_dict={'None':'off','D2':'old','D3':'on','D3-BJ':'bj','D4':'d4'}

    settings=dict()
    with open('rendered_WaNo.yml') as infile:
        WaNo_file = yaml.full_load(infile)
    
    settings['title']=WaNo_file['Title']
    settings['follow-up']=WaNo_file['Follow-up calculation']
    settings['int coord']=WaNo_file['Molecular structure']['Internal coordinates']
    settings['basis set']=WaNo_file['Basis set']['Basis set type']
    settings['use old mos']=WaNo_file['Initial guess']['Use old orbitals']
    settings['use old coord']=WaNo_file['Molecular structure']['Use old structure']
    settings['charge']=WaNo_file['Initial guess']['Charge']
    settings['multiplicity']=WaNo_file['Initial guess']['Multiplicity']
    settings['scf iter']=60
    settings['use ri']=WaNo_file['DFT options']['Use RI']
    settings['ricore']=WaNo_file['DFT options']['Memory for RI']
    settings['functional']=WaNo_file['DFT options']['Functional']
    settings['grid size']=WaNo_file['DFT options']['Integration grid']
    settings['disp']=disp_dict[WaNo_file['DFT options']['vdW correction']]
    settings['opt']=WaNo_file['Type of calculation']['Structure optimisation']
    settings['opt cyc']=50
    settings['tddft']=WaNo_file['Type of calculation']['TDDFT']
    settings['exc state type']=WaNo_file['Type of calculation']['TDDFT options']['Type of excited states']
    settings['num exc states']=WaNo_file['Type of calculation']['TDDFT options']['Number of excited states']
    settings['opt exc state']=WaNo_file['Type of calculation']['TDDFT options']['Optimised state']

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
    if multi != multi_new: print('The multiplicity was set to %i by default'%(multi_new))
    
    return multi_new

if __name__ == '__main__':
    
    settings=get_settings_from_rendered_WaNo()
    if settings['follow-up']: 
        os.system('mkdir old_results; tar -xf old_calc.tar.xz -C old_results')
        with open('old_results/rendered_WaNo.yml') as infile:
            old_settings = yaml.full_load(infile)
        settings['title']=old_settings['Title']

    coord_file='coord_0'
    if settings['use old coord']: os.system('cp old_results/coord %s'%(coord_file))
    else: os.system('x2t initial_structure.xyz > %s'%(coord_file))

    n_el=sum(ase.io.read(coord_file).numbers)-settings['charge']
    
    settings['multiplicity']=sanitize_multiplicity(settings['multiplicity'],n_el)

    define_done=tm.run_define(tm.make_define_str(settings,coord_file))
    if settings['follow-up']: os.system('rm -rf old_results')

    if not define_done:
        print('An error occured when running define:')
        with open('define.out') as infile:
            lines=infile.readlines()
        for line in lines: print(line)

    if settings['tddft'] and settings['opt']: os.system('adg exopt $i'%(settings['opt state']))

    if settings['use ri']: scf_program='ridft'
    else: scf_program='dscf'

    if settings['opt']: suffix='_0'
    else: suffix=''

    output=scf_program+suffix+'.out'
    done=False
    num_iter,max_iter=0,100

    while not done:
        #debug_step,num_iter=0,0
        done,err = tm.run_turbomole(scf_program,output)
        if not done: # put this part to tm.tun_turbomole ? (v.i.)
            print('Error while running %s:'%(scf_program))
            print(err)
            exit(0)
        os.system('eiger > eiger.out')
        done,err=tm.check_scf(output)

        if not done:
            if err == 'not converged': 
                num_iter+=settings['scf iter']
                if num_iter > max_iter: 
                    print('SCF not converged in maximum number of iterations (%i)'%(max_iter))
                    exit(0)
            elif err == 'negative HLG': 
                print('Attention: negative HOMO-LUMO gap found - please check manually')
                exit(0)
        #tm.setup_restart(err)

    if settings['tddft']:
        done,err=tm.run_turbomole('escf','escf%s.out'%(suffix))
        if not done: # put this part to tm.tun_turbomole ? (v.s.)
            print('Error while running %s:'%(scf_program))
            print(err)
            exit(0)
        
        done,err=tm.check_escf(output)
        while not done:
            # errors and handling thereof not yet implemented
            if not done: 
                print('Problem with escf calculation found - please check manually')
                exit(0)
    
    if settings['opt']:
        command='jobex'
        if settings['use ri']: command+=' -ri'
        if settings['tddft']: command+=' -ex %i'%(WaNo_file['state'])
        command+=' -c %i'%(settings['opt cyc'])
        
        done=False
        num_cycles,max_cycles=0,500

        while not done:
            done,err=tm.run_turbomole(command)
            if not done: # put this part to tm.tun_turbomole ? (v.s.)
                print('Error while running jobex - please check manually')
                print(err)
                exit(0)
            os.system('eiger > eiger.out')
            
            done,err=tm.check_opt()

            if not done:
                if err == 'opt not converged':
                    num_cycles+=settings['opt cyc']
                    if num_cycles > max_cycles:
                        print('Structure optimisation not converged in maximum number of cycles (%i)'%(max_cycles))
                        exit(0)
                else:
                    print('An error occurred during the structure optimisation - please check manually')
                    exit(0)
            
            elif not settings['tddft']: 
                scf_done,err=tm.check_scf('job.last')
                if not scf_done: 
                    print('The Structure optimisations converged but the last SCF run showed an error.')
                    exit(0)

    results_dict={}
    
    results_dict['title']=settings['title']
    results_dict['energy_unit']='Hartree'
    with open('energy') as infile: results_dict['energy'] = float(infile.readlines()[-2].split()[1])
    if settings['tddft']:
        results_dict['exc_type']=settings['exc state type']
        exc_energies=[]
        with open('exspectrum') as infile:
            exc_lines=infile.readlines()[2:]
        for exc_line in exc_lines: exc_energies.append(float(exc_line.split()[2]))
        results_dict['exc_energies']=exc_energies

    with open('results.yml','w') as outfile: yaml.dump(results_dict,outfile)

    output_files=['alpha','auxbasis','basis','beta','control','coord','energy','forceapprox','gradient','hessapprox','mos','optinfo','rendered_WaNo.yml']
    for filename in output_files:
        if not os.path.isfile(filename): output_files.remove(filename)

    os.system('tar -cf results.tar.xz %s'%(' '.join(output_files)))
