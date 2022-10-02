import os
import numpy as np
from matplotlib import pyplot as plt
houzui=os.sys.argv[1]

def read(file):
    with open(file,'r')as f:
        data=f.read()
        data=data.split()
    data=np.array(data[1:])
    data=data.astype(float)
    return data

os.system("cat var"+houzui+".txt|awk -F ' ' '{print$1}'>"+houzui+"r21 ")
os.system("cat var"+houzui+".txt|awk -F ' ' '{print$2}'>"+houzui+"r22 ")

r21=np.log10(read(houzui+'r21'))
r22=np.log10(read(houzui+'r22'))

#plt.scatter(range(len(r22/r21)),np.log(r22/r21))
#plt.plot([0,50],[0,0])
plt.figure(figsize=(8,8))
plt.title('Effect Of Correction')
plt.scatter(r21,r22,label='event')
plt.legend(loc='lower right')
plt.plot([min(r21),max(r22)],[min(r21),max(r22)],'--')
plt.axis('equal')
plt.xlim([-3,3])
plt.ylim([-3,3])
plt.xlabel('log10(Var(fit)) before correction')
plt.ylabel('log10(Var(fit)) after correction')
plt.text(1,-1,'Better',fontsize=20)
plt.text(-1,1,'Worse',fontsize=20)
plt.savefig('se'+houzui+'.png')
