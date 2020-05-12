import os
import os.path
import shutil
import fnmatch
import re
from cif import *

def getNelement(self):

    #chemical_formula_sum
    cf = parse_cif(self)
    cb = cf[0][1]

    formula=[]

    sumls = cb['_chemical_formula_sum']

    return sumls


rootdir = os.getcwd()
path = '/home/lits/ns2_work/test/Sn_file'



error = 0
lserror = []

decimal = 0
bingo = 0
total = 0

allls=[]
unils=[]

for root,dirnames,filenames in os.walk(path):
    for filename in fnmatch.filter(filenames,'*.cif'):
        try:
            luo = getNelement(path+'/'+filename)
            total+=1
        except:
            error = error+1
            print '----------------------------------------------------------'
            print filename
            print '----------------------------------------------------------'
            print '                                                          '
            lserror.append(filename)
        finally:
            allls.append(luo)

order=[]

for u in allls:
    if not u in unils:
        unils.append(u)

for o in range(len(unils)):
    order.append([])

for i in range(0,len(unils)):
    for j in range(0,len(allls)):
        if allls[j] == unils[i]:
            order[i].append(allls[j])
for k in order:
    print k

print 'error = ',error
print 'lserror = ',lserror
print 'decimalnum = ',decimal
print 'bingo = ',len(unils)
print 'total = ',total
print 'allls = ',len(allls)
print 'order = ',len(order)

unicount=0
copycount=0
total=0
indicator=[]
if not os.path.isdir(rootdir+'/'+'uniquefile'):
    os.mkdir(rootdir+'/'+'uniquefile')
if not os.path.isdir(rootdir+'/'+'copyfile'):
    os.mkdir(rootdir+'/'+'copyfile')
for boot,directory,strucnames in os.walk(path):
    for strucname in fnmatch.filter(strucnames,'*.cif'):
        try:
            luo = getNelement(path+'/'+strucname)
            total+=1
        except:
            error = error+1
            print '----------------------------------------------------------'
            print filename
            print '----------------------------------------------------------'
            print '                                                          '
            lserror.append(filename)
        finally:
            if not luo in indicator:
                indicator.append(luo)
                shutil.copy(path+'/'+strucname,rootdir+'/'+'uniquefile')
                unicount+=1
            else:
                shutil.copy(path+'/'+strucname,rootdir+'/'+'copyfile')
                copycount+=1
sum = unicount+copycount
print 'unicount = ',unicount
print 'copycount = ',copycount
print 'sum=',sum
print 'total=',total


