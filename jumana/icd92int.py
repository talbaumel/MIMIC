import sys

icd2int = {}
fin = open(sys.argv[1],'r')
for line in fin:
    tline = line.split('\t')
    icd2int[tline[0]] = tline[1]
fin.close()

fin = open(sys.argv[2],'r')

with open(sys.argv[3],'w') as fout:
    for line in fin:
        tline = line[:-1].split('|')
        fout.write('|'.join([icd2int[icd] for icd in tline if icd!='']))
        fout.write('\n')
fin.close()

