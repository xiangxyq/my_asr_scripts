rm -rf trans.txt wav.scp

for file in `find wav/ -name *.wav.txt`
do
utt=`echo $file | awk -F'/' '{print $3}'`
cmd=`cat $file` 
echo $utt
echo ${utt:0:16}
echo "${utt:0:16}	$cmd" >> trans.txt
echo "${utt:0:16}	${file:0:30}" >> wav.scp
done
#dos2unix trans.txt
#dos2unix wav.scp
