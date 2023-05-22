#!/usr/bin/env python

import mne
import matplotlib
import os
import argparse

def make_source_spaces(subject, sourcepath):

    #oct6 takes too long, oct5 slow but managable
    
    myss = mne.setup_source_space(subject,'oct6', surface='white', n_jobs=4)
    vol_src = mne.setup_volume_source_space(subject)
    
    mne.write_source_spaces(subject + '-src.fif',myss, overwrite=True)
    mne.write_source_spaces(subject + '-vol-src.fif',vol_src, overwrite=True)

def make_watershed(subject, sourcepath):

    mne.set_config('SUBJECTS_DIR', sourcepath)
    mne.bem.make_watershed_bem(subject, sourcepath, overwrite=True, atlas=False, gcaatlas=True, show=True)

def make_bem_models(subject, sourcepath):

    model = mne.make_bem_model(subject, conductivity=[0.3])
    bem_sol = mne.make_bem_solution(model)
    
    mne.write_bem_surfaces(subject + '-bem.fif', model, overwrite=True)
    mne.write_bem_solution(subject + '-bem-sol.fif', bem_sol, overwrite=True)


def run_qc(subject, sourcepath):
    current=os.getcwd()
    os.chdir(sourcepath)
    os.chdir(subject)
    os.system("freeview -v mri/T1.mgz -f bem/outer_skin.surf:edgecolor=red bem/outer_skull.surf:edgecolor=blue bem/inner_skull.surf:edgecolor=yellow --ss {}/{}_QC.jpg".format(current,subject))
    
    print("mris_expand watershed/{}_outer_skull_surface 1 {}_outer_skull_surface2".format(subject, subject))
    
    os.chdir(current)

def main():
    parser = argparse.ArgumentParser(
        prog="setup_sources_mne.py",
        description="Sets up the MNE source space and BEM",
        epilog="Conveninece functions by PJM"
    )

    parser.add_argument(
            '--subj',
            help='Subject Number',
            nargs=1,
            required=True,
        )
    parser.add_argument(
            '--fs_dir',
            help="freesurfer path",
            nargs=1,
        )
    parser.add_argument(
            '--ss',
            help="run source space setup parts",
            action=argparse.BooleanOptionalAction,
            default=True,
        )
    parser.add_argument(
            '--ws',
            help="run watershed parts",
            action=argparse.BooleanOptionalAction,
            default=True,
        )
    parser.add_argument(
            '--bem',
            help="only run BEM parts",
            action=argparse.BooleanOptionalAction,
            default=True,
        )
    parser.add_argument(
            '--qc',
            help="run QC image on watershed",
            action="store_true",
            default=False,
        )

    args = parser.parse_args()
    subj=args.subj[0]
    if args.fs_dir == None:
        sourcepath=os.getcwd() + "/freesurfer"
    else:
        print(args.fs_dir[0])
        sourcepath=args.fs_dir[0]
	
    print(subj)
    print("SourceSpace: {}".format(args.ss))
    print("Watershed: {}".format(args.ws))
    print("BEM: {}".format(args.bem))
    
    subject = args.subj[0]
    #sourcepath=os.getcwd() + "/freesurfer"
    mne.set_config('SUBJECTS_DIR', sourcepath)
    
    if args.ss == True:
        make_source_spaces(subj, sourcepath)
    if args.ws == True:
        make_watershed(subj, sourcepath)
    if args.bem == True:
        make_bem_models(subj, sourcepath)
    if args.qc == True:
        run_qc(subj, sourcepath)
    
    
    
    

if __name__ == '__main__':
	main()
