for y in 2013 2014 2015 2016 2017 
do
	for m in $(seq -w 1 12)
	do
		for d in $(seq -w 1 10 30)
		do
			echo $y$m$d
		done
	done
done


for y in 2018
do
	for m in $(seq -w 1 8)
	do
		for d in $(seq -w 1 7 30)
		do
			echo $y"0"$m$d
		done
	done
done
