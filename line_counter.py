def count_line(filename):
	with open(filename) as f:
		print 'line num is', len(f.readlines())

def count_file_num(dirpath):
	import os
	print 'file num in', dirpath, 'is', len(os.listdir(dirpath))

count_file_num('google_result')