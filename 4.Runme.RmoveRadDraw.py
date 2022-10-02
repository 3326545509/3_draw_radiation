#统计:同一地震事件 不同震中距(即不同台站)
from matplotlib import pyplot as plt
import os
import numpy as np
from obspy.core import UTCDateTime
import csv
from scipy import stats
from multiprocessing import Process

outdire='./6.rmRad/'
indire='./5.health/'
#houzuis=['20to17']
houzuis=['33to25','25to20','20to17','17to15','15to13.2','13.2to11.7','11.7to10',\
'10to8.5','8.5to7.3','7.3to6.4','6.4to5.5','5.5to4.8','4.8to4.25']

def read(file):
    dataf=[]
    datacatlog=[]
    with open(file) as csv_file:
        rows = csv.reader(csv_file)
        for row in rows:
            dataf.append(row)
    return dataf

def statistic(dataf):
    headf=dataf[0]
    ifdate=headf.index('date')
    iftime=headf.index('time')
    imag=headf.index('mag')
    idist=headf.index('dist')
    idepmax=headf.index('depmax')
    #irad=headf.index('rad')
    iid=headf.index('id')

    t0=UTCDateTime(dataf[1][ifdate]+'T'+dataf[1][iftime])
    events=[]
    event=[]
    #-----以事件为单位进行分类, 前提是:csv文件以事件为块储存,即相同事件为相邻行
    #------遍历csv中的每一行
    for i in range(1,len(dataf)):
        #------检查该记录和上一条记录是否为同时刻, 若为同时刻则计入同一个event
        t=UTCDateTime(dataf[i][ifdate]+'T'+dataf[i][iftime])
        if abs(t-t0)<5:
            event.append(dataf[i])
            print(i,' is added')
            if i==len(dataf)-1:
                events.append(event)
            continue
        if len(event)>=10:
            print('-----len event:',len(event))
            events.append(event)
        event=[]
        event.append(dataf[i])
        t0=t
    print('-----number of event,record>6: ',len(events))
    
    k=0
    for temp in events:
        k=k+len(temp)
    print('-----number of all sac:',k)
    return events#,idist,idepmax,imag,irad,ifdate,iftime

def process_a_period(houzui):
    file=indire+'3.health'+houzui+'.csv'
    data=read(file)
    events=statistic(data)
    per=float(houzui.split('to')[0])+float(houzui.split('to')[1])/2
    for event in events:
        print('===')
        os.system("cat "+file+"|awk -F ',' '{if(NR==1)print}'>3.health"+houzui+".csv")
        with open('3.health'+houzui+'.csv','a')as f:
            writer = csv.writer(f)
            for sac in event:
                writer.writerow(sac)
        #-------以上是为了将事件挨个读取出来, 以下处理单个事件
        os.system('sh 0.runme.sh '+houzui+' '+str(per))
    os.system('python3 5.showVAR.py '+houzui)

if __name__=='__main__':
    os.system('mkdir '+outdire)
    for houzui in houzuis:
        # pi=Process(target=process_a_period,args=(houzui,))
        # pi.start()
        process_a_period(houzui)



    # p=["a","b","c"]
    # i=1 
    # all_pi=[]
    # for pi in p:
    #     pi=Process(target=f,args=(pi,i,))
    #     pi.start()
    #     all_pi.append(pi)
    #     i=i+1
    # for temp in all_pi:
    #     temp.join()