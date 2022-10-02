import numpy as np
from matplotlib import pyplot as plt
import os
from scipy import stats

radfenjie=float(os.sys.argv[1])
time=os.sys.argv[2]
houzui=os.sys.argv[3]

def read(file):
    with open(file,'r')as f:
        data=f.read()
        data=data.split()
    data=np.array(data[1:])
    data=data.astype(float)
    return data

def var_fit(x,y,slope,intercept):
    y2=x*slope+intercept
    if x==[] or y==[]:
        return 0
    mean=sum((y2-y)**2)/len(y2)
    return mean


depmax  =read('0.'+ houzui+ 'depmax')
dist    =read('0.'+ houzui+ 'dist')
rad     =read('2_'+  houzui+ 'rad')
baz     =read('0.'+ houzui+ 'baz')
#xyz:全部数据
x=dist
y=depmax
z=rad
b=baz
#dist depmax rad: 剔除后的数据
dist=[]
depmax=[]
rad=[]
baz=[]
for i in range(len(z)):
    if z[i]<radfenjie:
        continue
    dist.append(x[i])
    depmax.append(y[i])
    rad.append(z[i])
    baz.append(b[i])
dist=np.array(dist)
depmax=np.array(depmax)
rad=np.array(rad)
baz=np.array(baz)

yall=np.log(y*np.sqrt(np.sin(x/6371)))
depmax_norad=np.log(depmax*np.sqrt(np.sin(dist/6371))/rad)

yall=yall-np.mean(yall)
depmax_norad=depmax_norad-np.mean(depmax_norad)
plt.figure(figsize=(20,10))
plt.cla()
plt.suptitle("Event: "+time)
plt.subplot(1,2,1)
plt.ylim([-3,3])
plt.xlim([0,800])
plt.xlabel('distance / km')
plt.ylabel('ln(amplitude)')

slope, intercept, r, p, se = stats.linregress(x,yall)
plt.plot(x,slope*np.array(x)+intercept,color='cyan')
var=var_fit(x,yall,slope,intercept)
plt.scatter(x,yall,c='cyan',label='Before correction'\
    +' var: '+"{0:.{1}e}".format(var, 3))


slope_norad, intercept_norad, r_norad, p_norad, se_norad = stats.linregress(dist,depmax_norad)
plt.plot(dist,slope_norad*np.array(dist)+intercept_norad,color='red')
var_norad=var_fit(dist,depmax_norad,slope_norad,intercept_norad)
plt.scatter(dist,depmax_norad,c='red',label='After correction'\
    +'    var: '+"{0:.{1}e}".format(var_norad, 3) )

plt.legend(loc='lower right')

#rows1: 辐射花样的角度(0-360)
#rows2: 辐射花样的大小
rows1=[]
rows2=[]
with open(houzui+'.rad','r')as f:
    data=f.read()
    data=data.splitlines()
    data=data[6:]
for temp in data:
    rows1.append(temp.split()[0])
    rows2.append(temp.split()[1])

rows1=np.array(rows1).astype(float)*2*np.pi/360
rows2=np.array(rows2).astype(float)

plt.subplot(1,2,2,projection='polar')
plt.scatter(b*np.pi/180,x,s=y*400/max(y),c='white',marker='o',edgecolors='black',label='Data excluded')
plt.scatter(baz*np.pi/180,dist,s=depmax*400/max(y),c='white',marker='o',edgecolors='red',label='Data remained')
plt.plot(rows1,rows2*800/max(rows2),label='Radiation')#,'go')
#plt.ylabel('distance / km')
plt.legend(loc='lower right')

plt.savefig('6.rmRad/'+time+"_"+houzui+'.png')
os.system('mv '+houzui+'.rad '+time+'.'+houzui+'.rad')

# with open('r2.statistic.txt','a')as f:
#     f.write(str(r**2) + " " + str(r_norad**2) + "\n")

with open('var'+houzui+'.txt','a')as f:
    f.write(str(var) + " " + str(var_norad) + "\n")
