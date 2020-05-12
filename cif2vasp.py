#!/usr/bin/env python
#_*_coding:utf-8_*_

__author__ = "Shulin Luo"
__date__ = "Feb. 22 2019"

#ABC cif2vasp

import numpy as np
from cif import *
import os
import os.path
import shutil
import fnmatch
import re

'''
Translate cif file into VASP
'''

def read_cif(filename):
    cf=parse_cif(filename)
    cb=cf[0][1]

    # lattice parameters
    aa=float(cb['_cell_length_a'])
    bb=float(cb['_cell_length_b'])
    cc=float(cb['_cell_length_c'])
    alpha=float(cb['_cell_angle_alpha'])
    beta=float(cb['_cell_angle_beta'])
    gamma=float(cb['_cell_angle_gamma'])
    alpha=alpha*(math.pi/180)
    beta=beta*(math.pi/180)
    gamma=gamma*(math.pi/180)

    # lattice vector
    lattice=[]
    lattice=lattice_vector(aa, bb, cc, alpha, beta, gamma)

    # elements
    typesymbol=[]
    elements=[]
    sltemp=[]
    if '_atom_type_symbol' in cb:
	sltemp=cb['_atom_type_symbol']
	for sl in sltemp:
	    m=re.match(r'[A-Za-z]{1,}',sl)
	    typesymbol.append(m.group())
	for ts in typesymbol:
	    if not ts in elements:
		elements.append(ts)
    else:
	for jj in ['_atom_site_label','_atom_site_type_symbol']:
	    if jj in cb:
		sltemp=cb[jj]
		break
	for sl in sltemp:
	    m=re.match(r'[A-Za-z]{1,}',sl)
	    typesymbol.append(m.group())
	for ts in typesymbol:
	    if not ts in elements:
		elements.append(ts)


    #formula
    formula=[]
    for formu in ['_chemical_formula_sum','_chemical_formula_structural']:
	if formu in cb:
	    formula=cb[formu]
	    break
	else:
	    formula='POSCAR'
    formula=formula

    # space group number
    group_number=None
    if '_space_group.it_number' in cb:
	group_number=str(cb['_space_group.it_number'])
    elif '_space_group_it_number' in cb:
	group_number=str(cb['_space_group_it_number'])
    elif '_symmetry_int_tables_number' in cb:
	group_number=str(cb['_symmetry_int_tables_number'])

    # space group H-M symbol
    symbolHM=None
    if '_space_group.Patterson_name_h-m' in cb:
	symbolHM=format_symbol(cb['_space_group.patterson_name_h-m'])
    elif '_symmetry_space_group_name_h-m' in cb:
	symbolHM=format_symbol(cb['_symmetry_space_group_name_h-m'])

    # symmetry operations
    for name in ['_space_group_symop_operation_xyz',
		'_space_group_symop.operation_xyz',
		'_symmetry_equiv_pos_as_xyz']:
	if name in cb:
	    sitesym=cb[name]
	    break
        else:
	    sitesym=None

    # numbers
    numbers=[]
    typenumbers=[]
    temele=[]
    sitesymbol=[]
    atomsitetp=[]
    for asts in ['_atom_site_label','_atom_site_type_symbol']:
	if asts in cb:
	    atomsitetp=cb[asts]
	    break
	else:
	    atomsitetp=None
    for ilabel in atomsitetp:
	m = re.match(r'[A-Za-z]{1,}',ilabel)
	sitesymbol.append(m.group())

    for jlabel in sitesymbol:
	if not jlabel in temele:
	    temele.append(jlabel)

    if '_atom_site_symmetry_multiplicity' in cb:
	typenumbers=cb['_atom_site_symmetry_multiplicity']
    elif sitesym:
	typenumbers=numbers_cal(sitesym, cb)
    elif symbolHM:
	typenumbers=numbers_cal(SG.get(symbolHM), cb)
    else:
	typenumbers=numbers_cal(SG.get(group_number), cb)

    numbers=[0]*len(temele)
    for kk in range(len(temele)):
	for kkk in range(len(sitesymbol)):
	    if sitesymbol[kkk]==temele[kk]:
		numbers[kk]+=int(typenumbers[kkk])

    sumnumbers=0
    for i in range(len(numbers)):
        sumnumbers+=int(int(numbers[i]))

    # positions
    typepositions=[]
    positions=[]
    if sitesym:
        typepositions=equival_pos(sitesym, cb)
    elif symbolHM:
        if SG.get(symbolHM):
            typepositions=equival_pos(SG.get(symbolHM), cb)
        else:
            raise SpacegroupNotFoundError('invalid spacegroup %s, not found in data base' %
                                                                                  (symbolHM,))
    elif group_number:
        typepositions=equival_pos(SG.get(group_number), cb)
    else:
        raise SpacegroupValueError('either *number* or *symbol* must be given for space group!')
    
    icd=0
    typecoord=[]
    for i in range(len(sitesymbol)):
        typecoord.append([])

    coord=[]
    for i in range(len(temele)):
        coord.append([])

    for s in range(len(sitesymbol)):
        for ss in range(typenumbers[s]):
            typecoord[s].append(typepositions[icd])
            icd+=1

    for ll in range(len(temele)):
        for lll in range(len(sitesymbol)):
            if sitesymbol[lll]==temele[ll]:
                coord[ll].append(typecoord[lll])

    for d in range (len(coord)):
        for dd in range(len(coord[d])):
            for ddd in range(len(coord[d][dd])):
                positions.append(coord[d][dd][ddd])

    def sortf(numbers,positions):
        pt=0
        groups=[[]]*len(numbers)
        for n in range(len(numbers)):
            groups[n]=[]
            groups[n].append(positions[pt:pt+numbers[n]])
            groups[n]=groups[n][0]
            pt+=numbers[n]
        def nlen(nm):
            return len(nm)
        numbers.sort()
        groups.sort(key=nlen)

        positions=[]
        for o in range(len(groups)):
            for p in groups[o]:
                positions.append(p)

        return numbers,positions
    nps=sortf(numbers,positions)

    print nps[0]
    print nps[1]
    print " "
    return formula,lattice,temele,nps[0],nps[1],sumnumbers

rootdir = os.getcwd()
path = rootdir+"/source"
total = 0
error = 0
success = 0
errorls = []

#clean
if os.path.isdir(rootdir+'/'+'VASPFILE'):
    os.system("rm  -r ./VASPFILE")
#write POSCAR
def write_poscar(filename):
    global error,success,errorls
    try:
        cif=read_cif(filename)
        #print cif
        if not os.path.isdir(rootdir+'/'+'VASPFILE'):
            os.mkdir(rootdir+'/'+'VASPFILE')
        f=open(rootdir+'/'+'VASPFILE'+'/'+filename.replace(path,'').split('.')[0]+'.vasp','w')
        f.write(cif[0]+'\n')
        f.write('1.0\n')
        
        for i in range(len(cif[1])):
            f.write(' ')
            for j in range(len(cif[1][i])):
                f.write('%12.9f ' %cif[1][i][j])
            f.write('\n')
        if len(cif[3])==1:
            f.write('C\n')
        if len(cif[3])==2:
            f.write('C  Ge\n')
        if len(cif[3])==3:
            f.write('C  Ge  O\n')
        if len(cif[3])==4:
            f.write('C  Cl  Ge   O\n')
        if len(cif[3])==5:
            f.write('C  Cl  Ge   K  O\n')
        if len(cif[3])==6:
            f.write('B  C  Cl  Ge  K    O\n')

        for j in range(len(cif[3])):
            f.write(' '+str(cif[3][j]))
        f.write('\n')
        f.write('Direct\n')
        for i in range(len(cif[4])):
            f.write(' ')
            for j in range(len(cif[4][i])):
                f.write('%12.9f ' %cif[4][i][j])
            f.write('\n')

        f.close()
        success+=1

    except:
        errorls.append(filename)
        error+=1
        if not os.path.exists(rootdir+'/abnormal'):
            os.makedirs(rootdir+'/abnormal')
            shutil.copy(filename,rootdir+'/abnormal')
        else:
            shutil.copy(filename,rootdir+'/abnormal')
    finally:
        pass

#WRITE
for root,dirnames,filenames in os.walk(path):
    for filename in fnmatch.filter(filenames,'*.cif'):
        total+=1
        write_poscar(path+'/'+filename)

#Print error list
print 'The number of total cif file = ',total
print 'The number of success = ',success
print 'The number of error = ',error
print 'The error list: ',errorls
