from pymatgen import Lattice, Structure
import numpy
from math import *
import xrayutilities as xru
from xrayutilities.materials.cif import CIFFile
from xrayutilities.materials.material import Crystal
from IPython.display import Image, display
from tempfile import NamedTemporaryFile
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os, sys
from ase.io import read

path = os.getcwd()

def read_file():  ##get POSCAR or cif files in one directory
    posList = []  ##list for poscar file
    cifList = []  ##list for cif file
    text1 = open("cif_path.txt", 'w')
    text2 = open("vasp_path.txt", 'w')
    for root, dirs, files in os.walk(path):
        for f in files:
            if f.split('.')[-1]=='cif':
                text1.writelines(os.path.join(root, f)+"\n")
                cifList.append(f)
            elif f.split('.')[-1]=='vasp' or 'POSCAR' in f:
                text2.writelines(os.path.join(root, f)+"\n")
                posList.append(f)
            else:
                pass
    text1.close()
    text2.close()
    return posList, cifList
#read_file()

def theta(filename, tmin=10, tmax=85):
    if not tmin or tmax:
        pass
    else:
        tmin=tmin
        tmax=tmax
    return numpy.arange(tmin, tmax, 0.01)

def get_cryinfo(filename):
    file = read(filename)
    formula = file.get_chemical_formula()
    recip_cell = file.get_reciprocal_cell()  ##array with size of 3*3
    norm_cell = file.get_cell_lengths_and_angles()  ##[a,b,c,alpha,belta,gamma]
    volume = file.get_volume()
    return formula, recip_cell, norm_cell, volume

def get_spgr(filename):
    file = open(filename, 'r')
    lines = file.readlines()
    for l in lines:
        if '_symmetry_Int_Tables_number' in l:
            spgr_num = int(l.split()[-1])
        else:
            pass
    file.close()
    return spgr_num

def calc_d(filename, h=1.0, k=1.0, l=1.0):
    norm_cell = get_cryinfo(filename)[2]
    v = get_cryinfo(filename)[3]
    a, b, c = norm_cell[0], norm_cell[1], norm_cell[2]
    alpha, belta, gamma = norm_cell[3], norm_cell[4], norm_cell[5]
    spgr_num = get_spgr(filename)
    d = 1.0
    if spgr_num in range(1,3):  ##triclinic
        d = (1.0/sqrt(v)*(sqrt(h)*sqrt(b)*sqrt(c)*sqrt(sin(alpha))+ \
                       sqrt(k)*sqrt(c)*sqrt(a)*sqrt(sin(belta))+ \
                       sqrt(l)*sqrt(a)*sqrt(b)*sqrt(sin(gamma))+ \
                       2.0*k*l*sqrt(a)*b*c*(cos(belta)*cos(gamma)-cos(alpha))+ \
                       2.0*h*l*sqrt(b)*a*c*(cos(alpha)*cos(gamma)-cos(belta))+ \
                       2.0*h*k*sqrt(c)*a*b*(cos(alpha)*cos(belta)-cos(gamma))))^(-1.0/2.0)
    elif spgr_num in range(3,16): ##monoclinic
        d = (sqrt(h)/(sqrt(a)*sqrt(sin(belta)))+sqrt(k)/sqrt(b)+ \
            sqrt(l)/(sqrt(c)*sqrt(belta))-2.0*h*l*cos(belta)/(a*c*sqrt(sin(belta))))**(-1.0/2.0)
    elif spgr_num in range(16,75): ##orthorhombic
        d = (sqrt(h)/sqrt(a)+sqrt(k)/sqrt(b)+sqrt(l)/sqrt(c))**(-1.0/2.0)
    elif spgr_num in range(75,143): ##tetragonal
        d = ((sqrt(h)+sqrt(k))/sqrt(a)+sqrt(l)/sqrt(c))**(-1.0/2.0)
    elif spgr_num in range(143,168): ##trigonal
        d = a/(((sqrt(h)+sqrt(k)+sqrt(l))*sqrt(sin(alpha))+2.0*(h*k+h*l+k*l)*(sqrt(cos(alpha))-sqrt(cos(alpha)))/ \
                                                       (1.0-3.0*sqrt(cos(alpha))+2.0*sqrt(cos(alpha))))**(1.0/2.0))
    elif spgr_num in range(168,195): ##hexagonal
        d = ((4.0/3.0)*(sqrt(h)+h*k+sqrt(k))/sqrt(a)+sqrt(l)/sqrt(c))**(-1.0/2.0)
    else: ##cubic
        d = a/((sqrt(h)+sqrt(k)+sqrt(l))**(1.0/2.0))

    return d

def hkl(filename):
    d = calc_d(filename, h, k, l)

def lorentz_f(theta):
    lorentz_factor = (1+cos(2*theta)**2)/(sin(theta)**2*cos(theta))
    return lorentz_factor

def creat_xrd(filename):   ##better to use cif file
    ##get lattice, composition, coordinate, atom_type
    file = read(filename)
    formula = file.get_chemical_formula()

    aim_cif = CIFFile(filename)
    aim_crystal = Crystal(name=formula, lat=aim_cif.SGLattice())

    two_theta = numpy.arange(18, 32, 0.01)
    #powder = xru.simpack.smaterials.Powder(aim_crystal, 1, crystallite_size_gauss=100e-9)
    powder = xru.simpack.Powder(aim_crystal, 1, crystallite_size_gauss=100e-9)
    pm = xru.simpack.PowderModel(powder, I0=10)
    intensities = pm.simulate(two_theta)
    print(two_theta, intensities)
    plt.plot(two_theta, intensities)
    plt.xlim(18, 32, 1)
    ax = plt.axes()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.4f'))
    plt.title("XRD Pattern for " + aim_crystal.name)
    plt.xlabel("2 theta (degree)")
    plt.ylabel("Intensity")
#    plt.savefig( "631.png", dpi=600)
    plt.show()
    
creat_xrd('/home/william/XRD/Experiment1/631.cif')
#creat_xrd('631.cif')
