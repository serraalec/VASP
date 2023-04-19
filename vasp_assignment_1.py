'''
Do single-point (static) energy calculation for H2 molecule at H-H bond length values of 0.6, 0.7, 0,8, 0.9, 1.0 angstrom, respectively. Retrieve the total energy out for each bond length value, and plot a curve with energy as vertical axis and bond length as horizontal axis. Then parabolically fits the curve and find the optimized bond length corresponding to the lowest energy. In your submission, please include the data table containing the bond lengths and energies, curve, parabolic fitting curve, and your optimized bond length.
'''
import os
import re
import shutil
import time


def sweep_it_up(bond_length):
    """
    Move everything to an analysis directory.
    """

    file_to_move = list(filter(lambda file: os.path.isfile(file), os.listdir()))

    if len(file_to_move) == 0:
        return

    new_dir = 'run_' + str(bond_length)
    os.mkdir(new_dir)
    for file in file_to_move:
        shutil.copyfile(file, new_dir + '/' + file)

    top = os.getcwd()
    
    os.chdir(new_dir)
    os.system('sbatch run.slurm')
    os.chdir(top)

def gen_POSCAR(bond_length):
    return '''H2 molecule 
1.0
16.0    0.0             0.0
0.0             16.0    0.0
0.0             0.0             16.0
  H
  2
cartesian
    
{pbond}         {bond}         {bond}
{bond}          {bond}         {bond}
    '''.format(bond=8.0, pbond=8.0+bond_length)

def sim_step(bond_length):
    with open('POSCAR', 'w') as p:
        p.write(gen_POSCAR(bond_length))
    sweep_it_up(bond_length)


def main():
    sim_step(0.6)
    sim_step(0.7)
    sim_step(0.8)
    sim_step(0.9)
    sim_step(1)   
    
    

if __name__ == '__main__':
    main()
