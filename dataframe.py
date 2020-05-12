import numpy as np 
import pandas as pd 
import json
def readjson(filepath):
    with open(filepath,'r') as file:
        content=json.load(file)
        print(content)
def creatcsv(filepath):
    df=pd.DataFrame(columns=["filename","spacegroup","amplitude", "hkl", "two_theta", "d_spacing"])
    df.to_csv(filepath)
def addcsv(cifpath,jsonpath):
    pass
    
# readjson('data/629.json')
creatcsv('data/database.csv')