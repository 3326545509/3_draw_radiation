houzui=$1
PER=$2
mkdir $houzui
datafile="./3.health"${houzui}".csv"

# #----period need computed
# cat > perfil << EOF
# 18.5
# 20
# 40
# EOF

# #----period need computed
# PER=18.5

#----define seismic moment
MOM=1.0e+26

#----define reference distance
DIST=1000
MODE=0
X0=5.0 ; Y0=5.0

echo 'rad'>"2_"${houzui}"rad"
#----NR in datafile.csv need computed
imax=`cat $datafile|wc -l`
i=2
while (($i<=$imax ))
do

HS=`cat ${datafile}|awk -F ',' '{if(NR=='$i')print$15}'`
DIP=`cat ${datafile}|awk -F ',' '{if(NR=='$i')print$19}'`
RAKE=`cat ${datafile}|awk -F ',' '{if(NR=='$i')print$20}'`
STK=`cat ${datafile}|awk -F ',' '{if(NR=='$i')print$18}'`
lo=`cat ${datafile}|awk -F ',' '{if(NR=='$i')print$5}'`
la=`cat ${datafile}|awk -F ',' '{if(NR=='$i')print$6}'`
baz=`cat ${datafile}|awk -F ',' '{if(NR=='$i')print$13}'`

#----la lo round----------------------------------------------
#----la round
zhengshu=`echo "scale=0; $la/1"|bc`
xiaoshu=`echo "$la-$zhengshu"|bc`
if [ `echo "$xiaoshu<=0.25"|bc` -eq 1 ] 
then
   fujia=0
elif [ `echo "$xiaoshu>0.25"|bc` -eq 1 ] && [ `echo "$xiaoshu<0.75"|bc` -eq 1 ]
then
   fujia=0.5
else
   fujia=1
fi
la=`echo "$zhengshu+$fujia"|bc`

#----lo round
zhengshu=`echo "scale=0; $lo/1"|bc`
xiaoshu=`echo "$lo-$zhengshu"|bc`
if [ `echo "$xiaoshu<=0.25"|bc` -eq 1 ] 
then
   fujia=0
elif [ `echo "$xiaoshu>0.25"|bc` -eq 1 ] && [ `echo "$xiaoshu<0.75"|bc` -eq 1 ]
then
   fujia=0.5
else
   fujia=1
fi
lo=`echo "$zhengshu+$fujia"|bc`
#----baz round
zhengshu=`echo "scale=0; $baz/1"|bc`
xiaoshu=`echo "$baz-$zhengshu"|bc`
if [ `echo "$xiaoshu<=0.5"|bc` -eq 1 ]
then
   fujia=0
else
   fujia=1
fi
baz=`echo "$zhengshu+$fujia"|bc`
#------------------------------------------------------------

#echo "HS  DIP  RAKE  STK  lo  la  baz"
#echo "$HS $DIP $RAKE $STK $lo $la $baz"

#----generate V model
sh 1.get_1D_model.sh $lo $la $houzui

#----eigenfunction computaion
{
mv "modcus"${houzui}".d" ${houzui}
cd ${houzui}
#sprep96 -M modcus.d -HS $HS -HR 0 -L -R -PARR perfil -NMOD 2
sprep96 -M "modcus"${houzui}".d" -HS $HS -HR 0 -L -R -PER $PER -NMOD 2
sdisp96
sregn96 -DER
#slegn96 -DER
}>/dev/null

#----radiaton computation
sdprad96 -R -DIP ${DIP} -RAKE ${RAKE} -STK ${STK} -DIST ${DIST} \
       -PER ${PER} -HS ${HS} -M ${MODE} -M0 ${MOM} \
	-X0 ${X0} -Y0 ${Y0} -V>"../"${houzui}".rad"
radfile=${houzui}".rad"
cd ..
# rad=`cat ${radfile} |awk -F ' ' '{if($1=='$baz')print$2}'`
# echo "$rad">>"2_"${houzui}"rad"
cat ${radfile} |awk -F ' ' '{if($1=='$baz')print$2}'>>"2_"${houzui}"rad"
echo "---$i  is ok"
let i++
done
echo ${houzui}$(date +%R)