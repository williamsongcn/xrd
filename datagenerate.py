import pandas as pd 
import random
import numpy as np
import csv
list1=[]
trainx=[]
for x in range(500):
    if x <100:
        trainx.append([[random.uniform(1,5),random.uniform(1,5),random.uniform(1,5)],[random.uniform(1,5),random.uniform(1,5),random.uniform(1,5)]])
        list1.append([x,[random.uniform(1,5),random.uniform(1,5),random.uniform(1,5)],[random.uniform(1,5),random.uniform(1,5),random.uniform(1,5)],1])
    if (x <200 and x >=100):
        trainx.append([[random.uniform(0,1),random.uniform(0,1),random.uniform(1,5)],[random.uniform(10,20),random.uniform(10,20),random.uniform(10,20)]])
        list1.append([x,[random.uniform(0,1),random.uniform(0,1),random.uniform(1,5)],[random.uniform(10,20),random.uniform(10,20),random.uniform(10,20)],2])

    if (x <300 and x >=200):
        trainx.append([[random.uniform(10,20),random.uniform(10,20),random.uniform(1,5)],[random.uniform(10,20),random.uniform(10,20),random.uniform(10,20)]])
        list1.append([x,[random.uniform(10,20),random.uniform(10,20),random.uniform(1,5)],[random.uniform(10,20),random.uniform(10,20),random.uniform(10,20)],3])
    if (x <400 and x >=300):
        trainx.append([[random.uniform(10,20),random.uniform(10,20),random.uniform(10,20)],[random.uniform(10,20),random.uniform(10,20),random.uniform(10,20)]])
        list1.append([x,[random.uniform(10,20),random.uniform(10,20),random.uniform(10,20)],[random.uniform(10,20),random.uniform(10,20),random.uniform(10,20)],4])
    if (x <500 and x >400):
        trainx.append([[random.uniform(10,20),random.uniform(10,20),random.uniform(10,20)],[random.uniform(1,2),random.uniform(1,2),random.uniform(1,2)]])
        list1.append([x,[random.uniform(10,20),random.uniform(10,20),random.uniform(10,20)],[random.uniform(1,2),random.uniform(1,2),random.uniform(1,2)],5])
# columns=['id', 'twotheta', 'intense', 'label']
# with open('train.csv','w',newline='')as f:
#     f_csv = csv.writer(f)
#     f_csv.writerow(columns)
#     f_csv.writerows(list1)

# print(type(list1))
# list1=np.array(list1)
# print(list1[3])
dataset=pd.DataFrame(data=list1, columns=['id', 'twotheta', 'intense', 'label'],dtype='object')

# trainx=np.array(trainx)
# train=pd.DataFrame(data=trainx, columns=['twotheta', 'intense'],dtype='float')
dataset.to_csv('train.csv')
# train.to_csv('train_X.csv')
# print(type(dataset[['twotheta','intense']][0][0]))
list2=[]
for x in range(10):
    if x <2:
        list1.append([x,[random.uniform(1,5),random.uniform(1,5),random.uniform(1,5)],[random.uniform(1,5),random.uniform(1,5),random.uniform(1,5)],1])
    if (x <4 and x >=2):
        list1.append([x,[random.uniform(0,1),random.uniform(0,1),random.uniform(1,5)],[random.uniform(10,20),random.uniform(10,20),random.uniform(10,20)],2])

    if (x <6 and x >=4):
        list1.append([x,[random.uniform(10,20),random.uniform(10,20),random.uniform(1,5)],[random.uniform(10,20),random.uniform(10,20),random.uniform(10,20)],3])
    if (x <8 and x >=6):
        list1.append([x,[random.uniform(10,20),random.uniform(10,20),random.uniform(10,20)],[random.uniform(10,20),random.uniform(10,20),random.uniform(10,20)],4])
    if (x <10 and x >8):
        list1.append([x,[random.uniform(10,20),random.uniform(10,20),random.uniform(10,20)],[random.uniform(1,2),random.uniform(1,2),random.uniform(1,2)],5])
dataset2=pd.DataFrame(data=list2, columns=['id', 'twotheta', 'intense', 'label'],dtype='object')
dataset2.to_csv('test.csv')