import numpy as np
import os

#----输入为Tibet速度模型
model2_file=os.sys.argv[1]#model2_file="1_lola_97_22"
#----输出为Tibet和Prem合并的模型
houzui=os.sys.argv[2]
output="merge"+houzui+".model"

#----读取模型,保存为array
with open('PREM_1s.csv','r')as f:
    model1=f.readlines()
    model1=model1[2:]
    for i in range(len(model1)):
        model1[i]=model1[i].split(",")

with open(model2_file,'r')as f:
    model2=f.readlines()
    for i in range(len(model2)):
        model2[i]=model2[i].split()
#-----除去list中的换行符\n
for i in range(len(model1)):
    model1[i][9]=model1[i][9][:-1]

model1=np.array(model1).astype(float)
model2=np.array(model2).astype(float)
model3=[]
for i in range(len(model2)):
    try:
        H=model2[i+1][0]-model2[i][0]
    except:
        H=10
    #-----厚度为0的层不要
    if H==0:
        continue
    Vs=model2[i][1]
    Vp=model2[i][2]
    rh=model2[i][3]
    d2=model2[i][0]
    for j in range(len(model1)-1):
        d1=model1[j][1]
        #----在Prem中寻找Tibet对于对层(即深度相差0.5公里一下的), 把Q值模型给Tibet
        if (abs(d1-d2)<=0.5):
            if(abs(model1[j+1][1]-d2)<abs(d1-d2)):
                Qu=model1[j+1][8]
                Qp=model1[j+1][9]
            else:
                Qu=model1[j][8]
                Qp=model1[j][9]
            break
        else:
            continue
    #----temp即为生成的一层的模型
    temp=str(H)+" "+str(Vp)+" "+str(Vs)+" "+str(rh)+" "+\
        str(Qp)+" "+str(Qu)+" "+"0 0 1 1"
    model3.append(temp)

#----tibet模型最深到280, 280以下用Prem模型接上
for i in range(len(model1)-1):
    
    if model1[i][1]<=280:
        continue
    H=round(model1[i+1][1]-model1[i][1],1)
    if H==0:
        continue
    Vp=model1[i][2]
    Vs=model1[i][5]
    rh=model1[i][1]
    Qu=model1[i][8]
    Qp=model1[i][9]
    temp=str(H)+" "+str(Vp)+" "+str(Vs)+" "+str(rh)+" "+\
        str(Qp)+" "+str(Qu)+" "+"0 0 1 1"
    model3.append(temp)
with open(output,"w")as f:
    f.write("\n".join(model3))
