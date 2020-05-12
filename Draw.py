#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: William
Date: Nov 4th 2019
'''
import json
import matplotlib.pyplot as plt 
def Plot(file):
    diffrac=None
    with open(file,'r') as f:
        diffrac=json.load(f)
    
    plt.figure()
    plt.xlabel('2Θ')
    plt.ylabel('I')
    pattern=diffrac['pattern']
    DiTheta=[x[2] for x in pattern if x[2] < 90 ]
    Itensity=[y[0] for y in pattern if y[2] < 90]
    plt.plot(DiTheta,Itensity,'-')
    plt.show()

Plot('/home/william/XRD/Experiment1/json_file/629.json')
