import sys
try:
    IP = str(sys.argv[1]).strip(' ')
    PORT = int(sys.argv[2])
except:
    sys.exit("Input args error!")

f = open('info_db.para', 'w')
f.write(str(IP) + '\n')
f.write(str(PORT))
f.close()

