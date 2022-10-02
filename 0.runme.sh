#cat all.csv|awk -F ',' '{if(NR==1)print}'>3.merge.20to17.csv
#cat all.csv|awk -F ',' '{if(NR>=484&&NR<=526)print}'>>3.merge.20to17.csv

houzui=$1
per=$2

sacfile="./3.health"$houzui".csv"

cat $sacfile |awk -F ',' '{print$10}'>"0."${houzui}"depmax"
cat $sacfile |awk -F ',' '{print$9}'>"0."${houzui}"dist"
cat $sacfile |awk -F ',' '{print$13}'>"0."${houzui}"baz"

sh 2.eigen_rad.sh ${houzui} ${per}

radfile=${houzui}".rad"
time=`cat ${sacfile} |awk -F ',' '{if(NR==2)print$3"T"$4}'`
#----定义剔除的标准----
radmin=`cat ${radfile}|awk -F '' '{if(NR>6)print}'|sort -g -k2|awk -F ' ' '{if(NR==1)print$2}'`
radmax=`cat ${radfile}|awk -F '' '{if(NR>6)print}'|sort -g -k2|awk -F ' ' '{if(NR==361)print$2}'`
radmin=`echo "${radmin}"| awk '{printf("%f",$0)}'`
radmax=`echo "${radmax}"| awk '{printf("%f",$0)}'`
#==============================================
#-----一般情况剔除1/3
# radfenjie=`echo "scale=10; ($radmax-$radmin)/3+$radmin"|bc`
#------圆 不剔除
# if [ `echo "($radmax-$radmin)*0.8<=$radmin"|bc` -eq 1 ]
# then
#    radfenjie=$radmin #`echo "scale=10; ($radmax-$radmin)/5+$radmin"|bc`
# fi
# # #-------近似为园 则不剔除
# # if [ `echo "($radmax-$radmin)*2<=$radmin"|bc` -eq 1 ]
# # then
# #    radfenjie=$radmin
# # fi
# #-------节点处的突变很大,剔除1/2max
# if [ `echo "$radmax>=10*$radmin"|bc` -eq 1 ]
# then
#    radfenjie=`echo "scale=10; $radmax*0.8"|bc`
# fi

# if [ `echo "($radmax-$radmin)>=0.5*$radmin"|bc` -eq 1 ]
# then
#    radfenjie=$radmin #`echo "scale=10; ($radmax-$radmin)/5+$radmin"|bc`
# fi
# #-------近似为园 则不剔除
#==============================================
#-----从上到下, 逐渐由圆变8----
if [ `echo "($radmax-$radmin)>=0.5*$radmin"|bc` -eq 1 ]
then
   radfenjie=`echo "scale=10; ($radmax-$radmin)/8+$radmin"|bc`
else
   radfenjie=$radmin
fi
#-----
if [ `echo "($radmax-$radmin)>=1*$radmin"|bc` -eq 1 ]
then
   radfenjie=`echo "scale=10; ($radmax-$radmin)/5+$radmin"|bc`
fi
#-----
if [ `echo "($radmax-$radmin)>=1.5*$radmin"|bc` -eq 1 ] #2->1.5
then
   radfenjie=`echo "scale=10; ($radmax-$radmin)/4+$radmin"|bc`
fi
#-----
if [ `echo "($radmax-$radmin)>=8*$radmin"|bc` -eq 1 ]
then
   radfenjie=`echo "scale=10; ($radmax-$radmin)*0.7+$radmin"|bc`
fi

#mkdir 6.rmRad
python3 3.SingleDraw.py ${radfenjie} ${time} ${houzui}