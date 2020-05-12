import numpy as np 
import matplotlib.pyplot as plt 
from itertools import cycle 
from sklearn import svm,datasets
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import label_binarize
from sklearn.multiclass import OneVsRestClassifier
from scipy import interp
import pandas as pd 
from ast import literal_eval
import csv
trainData=pd.read_csv('train.csv')
label=trainData['label']
Y=label_binarize(label,classes=[1,2,3,4,5])
data=trainData[['twotheta','intense']].values.tolist()
train_X=[]
for x in data:
    listx=[]
    for y in x:
        listx+=literal_eval(y)
    train_X.append(listx) 
i=len(train_X)
j=len(train_X[0])
n_classes = Y.shape[1]
n_samples, n_features = i,j
random_state = np.random.RandomState(0)
X_train, X_test, y_train, y_test = train_test_split(train_X, Y, test_size=.5,random_state=0)
model = OneVsRestClassifier(svm.SVC(kernel='linear', probability=True,random_state=random_state))
clt = model.fit(X_train, y_train)
print(np.argmax(clt.decision_function(X_test), axis=1)[:5])



