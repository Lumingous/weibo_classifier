filenames = ['./textfile/segMovieTest','./textfile/segOtherTest']
with open('./textfile/segCombineTest', 'w') as outfile:
	for f in filenames:
		with open(f) as infile:
			for line in infile:
				outfile.write(line)
