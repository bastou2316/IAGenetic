Genetic algorith for PVC

command:
	python BurriDaMotaMarques.py [-n, --nogui] [-m, --maxtime] [filepath]

exemple:
	python BurriDaMotaMarques.py -n -m 1 ./data&pb005.txt

Use:
	Args:
		-n, --nogui		if you don't want user interface
		-m, --maxtime	number of seconds algorithm takes at mas, 
						expects an integer number after
		filepath		file to parse towns with this syntax:
							name1 x1 y1
							name2 x2 y2

Or type:
	python BurriDaMotaMarques.py -h
		or
	python BurriDaMotaMarques.py --help