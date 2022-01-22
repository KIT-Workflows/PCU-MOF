import os,sys,yaml
import subprocess

#function definitions

def utf8_enc(var):
    if sys.version_info >= (3, 0): return var.encode('utf-8')
    else: return var

def utf8_dec(var):
    if sys.version_info >= (3, 0): return var.decode('utf-8')
    else: return var

def make_define_str(settings,coord):
    
    if settings['use old mos']:
        with open('old_results/rendered_WaNo.yml') as infile:
            old_settings = yaml.full_load(infile)
        same_basis = old_settings['Basis set']['Basis set type'] == settings['basis set']

    if not (settings['use old mos'] and same_basis):
        define_string='\n%s\na %s\n'%(settings['title'],coord)
        #implement symmetry
        if settings['int coord']: define_string+='ired\n*\n'
        else: define_string+='*\nno\n'

        define_string+='b all %s\n*\n'%(settings['basis set']) # add options for basis sets (different for different atoms)

        if not settings['use old mos']:
            define_string+='eht\n\n'
            define_string+='%i\n'%(settings['charge'])
            #implement symmetry
            if settings['multiplicity'] < 3: define_string+='\n\n\n'
            else: define_string+='n\nu %i\n*\n\n'%(settings['multiplicity']-1)
        else: 
            define_string+='use old_results/control\n\n'

        define_string+='scf\niter\n%i\n\n'%(settings['scf iter'])
        if settings['use ri']: define_string+='ri\non\nm %i\n\n'%(settings['ricore'])
        if settings['functional'] != 'None': define_string+='dft\non\nfunc %s\ngrid %s\n\n'%(settings['functional'],settings['grid size'])
        if settings['disp'] != 'off': define_string+='dsp\n%s\n\n'%(settings['disp'])

        if settings['tddft']:
            define_string+='ex\n'
            if settings['multiplicity'] > 1: define_string+='urpa\n*\n'
            else: define_string+='rpa%s\n*\n'%(settings['exc state type'][0].lower())
            define_string+='a %i\n*\n'%(settings['num exc states'])
            define_string+='*\n\n'
            #implement symmetry
        define_string+='*\n'
    
    else:
        output_files=['alpha','auxbasis','basis','beta','control','mos']
        for filename in output_files:
            if os.path.isfile('old_results/%s'%(filename)): os.system('cp old_results/%s .'%(filename))
        os.system('cp coord_0 coord')
        define_string='\n\n\n\n\n'
        if settings['use ri']: define_string+='ri\non\nm %i\n\n'%(settings['ricore'])
        else: define_string+='ri\noff\n\n'
        if settings['functional'] != 'None': define_string+='dft\non\nfunc %s\ngrid %s\n\n'%(settings['functional'],settings['grid size'])
        else: define_string+='dft\noff\n\n'
        define_string+='dsp\n%s\n\n'%(settings['disp'])
        
        if not settings['tddft']:
            if old_settings['Type of calculation']['TDDFT']:
                os.system('sed -i \'s/#$max/$max/g\' control')
                for dg in 'soes','scfinstab','rpacor','denconv': os.system('kdg %s'%(dg))

        elif not old_settings['Type of calculation']['TDDFT']:
            define_string+='ex\n'
            if settings['multiplicity'] > 1: define_string+='urpa\n*\n'
            else: define_string+='rpa%s\n*\n'%(settings['exc state type'][0].lower())
            define_string+='a %i\n*\n'%(settings['num exc states'])
            define_string+='*\n\n'
            #implement symmetry
        else: 
            define_string+='ex\n'
            if old_settings['Type of calculation']['TDDFT options']['Type of excited states'] != settings['exc state type']:
                if settings['multiplicity'] > 1: define_string+='urpa\n'
                else: define_string+='rpa%s\n'%(settings['exc state type'][0].lower())
            define_string+='*\n'
            define_string+='a %i\n*\n'%(settings['num exc states'])
            define_string+='*\n\n'

        define_string+='*\n'

    return define_string

def run_define(define_string):

    define_process=subprocess.Popen(['define'],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    out, err = define_process.communicate(input=utf8_enc(define_string))
    with open('define.out','w') as outfile: outfile.write(utf8_dec(out))
    if 'normally' in utf8_dec(err).split(): return True
    else: return False

def run_turbomole(command,outfile=None):
    if outfile == None: outfile=command.split()[0]+'.out'
    
    proc_cmd=['nohup']+command.split()
    if not command.startswith('jobex'):
        if outfile == None: outfile = command+'.out'
        proc_cmd+=['>','outfile']

    with open(outfile,'w') as tm_out:
        tm_process=subprocess.Popen(proc_cmd,stdout=tm_out,stderr=subprocess.PIPE)
        out, err = tm_process.communicate()

    err=utf8_dec(err)

    if not 'normally' in err.split('\n')[-2].split(): return False,err
    else: return True,None

def check_scf(output_file):
    conv=False
    with open(output_file,'r') as infile:
        for line in infile.readlines():
            if 'convergence criteria cannot be satisfied' in line:
                conv=False
                break
            if 'convergence criteria satisfied' in line:
                conv=True
                break

    if conv == False:
        return False, 'not converged'
    else:
        with open('eiger.out','r') as infile:
            for line in infile.readlines():
                if 'Gap' in line:
                    hlg=float(line.split()[-2])
                    break
    if hlg < 0: return False, 'negative HLG'
    else: return True,None

def check_escf(output_file):
    conv=False
    with open(output_file,'r') as infile:
        for line in infile.readlines():
            if 'all done' in line:
                conv=True
                break
    return conv,None

def check_opt():
   
    conv=os.path.isfile('GEO_OPT_CONVERGED')

    if not conv:
        if os.path.isfile('GEO_OPT_RUNNING'): err = 'jobex did not end properly'
        else:
            with open('GEO_OPT_FAILED','r') as infile:
                for line in infile.readlines():
                    if 'OPTIMIZATION DID NOT CONVERGE' in line:
                        err = 'opt not converged'
                        break
                    #other errors need to be implemented
    else: err='' # check for problems with last run here, e.g. neg. HLG
    
    return conv,err 

def man_occ(occ_vec):
    if settings['multiplicity'] == 1:
        instring='\n\n\ny\neht\n0\n\n'
        define_process=subprocess.Popen(['define'],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        define_out=define_process.communicate(input=instring)[0].decode('utf-8').split('\n')
        for line in define_out:
            if 'NUMBER OF ELECTRONS IN YOUR MOLECULE IS' in line:
                n_occ=int(line.split()[-1])/2
                break
        instring+='c 1-%i\n'%(n_occ-len(occ_vec))
        for i in len(occ_vec):
            if occ_vec[i] == 1: instring+='c %i\n'%(n_occ-len(occ_vec)+1+i)
        instring+='*\n\n*\n'

     

    else: raise Error("manual occupation not implemented for open-shell systems")

