'''
Do single-point (static) energy calculation for H2 molecule at H-H bond length values of 0.6, 0.7, 0,8, 0.9, 1.0 angstrom, respectively. Retrieve the total energy out for each bond length value, and plot a curve with energy as vertical axis and bond length as horizontal axis. Then parabolically fits the curve and find the optimized bond length corresponding to the lowest energy. In your submission, please include the data table containing the bond lengths and energies, curve, parabolic fitting curve, and your optimized bond length.
'''
import os
import shutil
import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize

def sweep_it_up(bond_length):
    """
    Move everything except for this file, karanicolas_dihe_parm.dat to a debug directory.
    """
    file_to_move = list(filter(lambda file: os.path.isfile(file), os.listdir()))
    if len(file_to_move) == 0:
        return
    for file in file_to_move:
        shutil.copyfile(file, new_dir + '/' + file)


def grab_energy(length):
    top = os.getcwd()
    os.chdir('run_' + str(length))
    run_file = list(filter(lambda file: os.path.isfile(file) and
                       file.startswith('slurm') and
                       file.endswith('.out'), os.listdir()))[0]
    print(run_file)
    of = ''
    with open(run_file) as f:
        of = f.read()
    os.chdir(top)
    return of

def parse_energy(output):
    energy = output[output.find('E0= ')+len('E0= '):].split(' ')[0] 
    return energy

global fit

def quad(x):
    return fit[0]*x*x + fit[1]*x + fit[2]

def main():
    bond_lengths = {0.6, 0.7, 0.8, 0.9, 1.0}
    bond_energy_output = {}
    energy = {}
    for bond_length in sorted(bond_lengths):        
        bond_energy_output[bond_length] = grab_energy(bond_length)
        energy[bond_length] = float(parse_energy(bond_energy_output[bond_length]))
        

    print(energy.keys())
    x = list(energy.keys())
    y = list(energy.values())
    plt.plot(x, y, 'bx', label='datapoints')
    

    global fit
    fit = np.polyfit(x, y, 2)
    xx = np.linspace(0.6, 1.0, 1000)
    yy = quad(xx)

    latex = '$P(x) = {a:.2f}x^2 +{b:.2f}x + {c:.2f}$'.format(a = fit[0], b= fit[1], c=fit[2])
    
    plt.plot(xx, yy, label=latex,
             c = 'red')
    minimum = optimize.minimize(quad, 0.7).x[0]

    plt.plot(minimum, quad(minimum), 'kx', label='min x={x:.2f}'.format(x = minimum))

    plt.legend()
    plt.savefig('output.png')

    for i in range(len(x)):
        print('<tr> \n\t <td>')
        print(x[i])
        print('\n\t</td>\n\t<td>')
        print(y[i])
        print('\n\t</td>\n\t</tr>')       
    
if __name__ == '__main__':
    main()
