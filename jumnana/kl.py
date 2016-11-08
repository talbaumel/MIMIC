import numpy as np
import nltk, sys


labels2_file_name = sys.argv[1]#'MIMIC2/stats/codes_count_global'
labels3_file_name = sys.argv[2]#'MIMIC3/stats/codes_count_global'


def read_label_file(file_name):
    d = nltk.FreqDist()
    for line in open(file_name):
        line = line.strip().split()
        code, count = line[0], int(line[1])
        d[code] = count
    return nltk.SimpleGoodTuringProbDist(d), d.keys()

def kl(p, q, keys):
    return sum(map(lambda i: p.prob(i)*np.log(p.prob(i)/q.prob(i)), keys))

if __name__ == '__main__':
    d2, keys2 = read_label_file(labels2_file_name)
    d3, keys3 = read_label_file(labels3_file_name)
    keys = set(keys2+keys3)
    print kl(d3, d2, keys)