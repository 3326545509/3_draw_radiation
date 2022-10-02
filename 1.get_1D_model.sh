#merge PREM and Tibet velocity model
#sh XXX.sh lo la eg: sh XXX.sh 97 22
#output: a model file named modcus.d

if [ $# -ne 3 ]
then
	echo "Parameters needed, eg sh XXX.sh 97 22"
	exit 8
fi

longtitude=$1
latitude=$2
houzui=$3

outfile="1_lola_"${longtitude}"_"${latitude}

cat SWChinaVs_CUM_2020.txt |awk -F ' ' \
	'{if($1=='${longtitude}' && $2=='${latitude}')print$3"\t"$4"\t"$5"\t"$6}'>${outfile}

python3 1.a.get_model.py ${outfile} ${houzui}
cat > "modcus"${houzui}".d" << EOF
MODEL
CUS Model
ISOTROPIC
KGS
FLAT EARTH
1-D
CONSTANT VELOCITY
LINE08
LINE09
LINE10
LINE11
HR      VP      VS  RHO QP  QS  ETAP ETAS FREFP FREFS
EOF
cat "merge"${houzui}".model">>"modcus"${houzui}".d"
#rm "merge"${houzui}".model"
