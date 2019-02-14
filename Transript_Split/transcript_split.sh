for file in `find wav/ -name *.wav.txt`
do
	cmd=`cat $file` 
	cat fenci.txt | while read line 
	do
		utt=`echo $line | awk -F':' '{print $1}'`
		fenci=`echo $line | awk -F':' '{print $2}'`

		if [ "${cmd}" = "${utt}" ];then
			echo $fenci > $file
		fi
done

done

