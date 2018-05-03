import multiprocessing as mp
import twt3CDB
import sys

if __name__ == "__main__":
	size_arg = len(sys.argv)
	id = 0
	for item in sys.argv:
		if id == 0:
			id += 1
			continue
		else:
			print "create process for :" + item
			p = mp.Process(target = twt3CDB.subproc, args = (item, id%3))
			p.daemon = True
			p.start()
			id += 1
	print "All processes allocated"
	p.join()
	print "All processes exited"