import sys
try:
    num = int(sys.argv[1])
    IP = str(sys.argv[2]).strip(' ')
    PORT = int(sys.argv[3])
except:
    sys.exit("Input args error!")


f = open('info_analyzer.para', 'r')
PARA = f.readlines()
MACHINE_TOTAL = int(PARA[1])
MAXIMUM_QUERY = int(PARA[2])
INTERVAL = int(PARA[3])
f.close()


f = open('info_analyzer.para', 'w')
f.write(str(num) + '\n')
f.write(str(MACHINE_TOTAL) + '\n')
f.write(str(MAXIMUM_QUERY) + '\n')
f.write(str(INTERVAL) + '\n')
f.write(str(IP) + '\n')
f.write(str(PORT))
f.close()

import nltk
nltk.download('popular')
