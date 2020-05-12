#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 4  2019

@author: william
"""

from pymatgen import Lattice, Structure
import numpy as np
from math import *
import xrayutilities as xru
from xrayutilities.materials.cif import CIFFile
from xrayutilities.materials.material import Crystal
from tempfile import NamedTemporaryFile
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os, sys
from ase.io import read
import json
import threading


def read_file(SpecimenDir):  ##get POSCAR or cif files in one directory
    posList = []  ##list for poscar file
    cifList = []  ##list for cif file
    # if not os.path.exists(SpecimenDir+"/cif_path.txt"):

    text1 = open(SpecimenDir+"/cif_path.txt", 'w')
    text2 = open(SpecimenDir+"/vasp_path.txt", 'w')
    for root, dirs, files in os.walk(SpecimenDir):
        for f in files:
            if f.split('.')[-1]=='cif':
                text1.writelines(os.path.join(root, f)+"\n")
                cifList.append(os.path.join(root, f))
            elif f.split('.')[-1]=='vasp' or 'POSCAR' in f:
                text2.writelines(os.path.join(root, f)+"\n")
                posList.append(os.path.join(root, f))
            else:
                pass
    text1.close()
    text2.close()
    return posList, cifList

def get_spgr(filepath):
    file = open(filepath, 'r')
    lines = file.readlines()
    is_hex = False
    for l in lines:
        if '_symmetry_Int_Tables_number' in l:
            spgr_num = int(l.split()[-1])
        else:
            pass
    if spgr_num in range(168, 195):
        is_hex = True
    else:
        pass
    file.close()
    return is_hex
    
def generate(filepath):
    file = read(filepath)
    formula = file.get_chemical_formula()
    aim_cif = CIFFile(filepath)
    aim_crystal = Crystal(name=formula, lat=aim_cif.SGLattice())

    two_theta = np.arange(0, 90, 0.01)
    powder = xru.simpack.smaterials.Powder(aim_crystal, 1, crystallite_size_gauss=100e-9)
    #powder = xru.simpack.Powder(aim_crystal, 1, crystallite_size_gauss=100e-9)
    pm = xru.simpack.PowderModel(powder, I0=10)
    pd=xru.simpack.PowderDiffraction(aim_crystal)
    
    hkls_all = list(pd.data.keys())
    tmp_Amlist = []
    HKLs = []

    xrd_dict = {"meta": ["amplitude", "hkl", "two_theta", "d_spacing"], \
                    "created_at": "2019-04", \
                    "wavelength": {"element": "Cu", "in_angstroms": 1.54184}, 
                    "pattern": []}
    
    tmp_Amlist = list(float(pd.data[i]['r']) for i in hkls_all)
    Am_max = max(tmp_Amlist)

    for i in hkls_all:
        if pd.data[i]['active'] is True:
            HKLs.append(i)
    for j in range(len(HKLs)):
        theta = pd.data[HKLs[j]]['ang']
        Amplitude = pd.data[HKLs[j]]['r'] / float(Am_max) * 100
        d_spacing = pd.wavelength / (2 * sin(pd.data[HKLs[j]]['ang'] * pi / 180))
        hkls = []
        for i in HKLs[j]:
            hkls.append(float(i))
        xrd_list = [Amplitude, hkls, theta*2, d_spacing]
        xrd_dict['pattern'].append(xrd_list)
    
    return xrd_dict

def GroupGenerate(SpecimenDir):
    SpecimenDir=os.path.abspath(SpecimenDir)

    cifList=read_file(SpecimenDir)[-1]

    if os.path.exists(SpecimenDir+'/json_file'):
        pass
    else:
        command='mkdir '+SpecimenDir+'/json_file'
        os.system(command)
    for filepath in cifList:
        filename=os.path.basename(filepath)
        jsonname=filename.split('.')[0]+'.json'
        jsonpath=SpecimenDir+'/json_file/'+jsonname
        xrd_dict=generate(filepath)
        json_file=open(jsonpath,'w')
        json.dump(xrd_dict, json_file)
        json_file.close()


















