import os
import numpy as np
from matplotlib import pyplot as plt
#houzui=os.sys.argv[1]

def read(file):
    with open(file,'r')as f:
        data=f.read()
        data=data.split()
    data=np.array(data[1:])
    data=data.astype(float)
    return data
houzuis=['33to25','25to20','20to17','17to15','15to13.2','13.2to11.7','11.7to10',\
'10to8.5','8.5to7.3','7.3to6.4','6.4to5.5','5.5to4.8','4.8to4.25']
for houzui in houzuis:
    os.system("cat var"+houzui+".txt|awk -F ' ' '{print$1}'>"+houzui+"r21 ")
    os.system("cat var"+houzui+".txt|awk -F ' ' '{print$2}'>"+houzui+"r22 ")

    r21=np.log10(read(houzui+'r21'))
    r22=np.log10(read(houzui+'r22'))

    #plt.scatter(range(len(r22/r21)),np.log(r22/r21))
    #plt.plot([0,50],[0,0])
    plt.figure(figsize=(8,8))
    plt.title('Effect Of Correction  Period:'+houzui+'s')
    plt.scatter(r21,r22,label='event')
    plt.legend(loc='lower right')
    plt.plot([min(r21),max(r22)],[min(r21),max(r22)],'--')
    plt.axis('equal')
    plt.xlim([-2,2])
    plt.ylim([-2,2])
    plt.xlabel('log10(Var(fit)) before correction')
    plt.ylabel('log10(Var(fit)) after correction')
    plt.text(0.8,-0.8,'Better',fontsize=20)
    plt.text(-0.8,0.8,'Worse',fontsize=20)
    plt.savefig('se'+houzui+'.png')
