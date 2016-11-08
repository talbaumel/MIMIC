from nltk import FreqDist
import re
MIMIC_PATH = 'MIMIC3/MIMIC_PREPROCESSED'


def mimic_doc_yielder(mimic_path):
    for line in open(mimic_path):
        line = line.split('|')
        codes = line[0].split(',')#map(lambda code: re.sub(r'[^a-zA-Z0-9\.]', '', code), re.split(r'[ ,]', line[0]))
        text = (' '.join(line[1:])).split()
        yield codes, text

def write_fd_to_file(fd, file_name):
    with open(file_name, 'w') as fp:
        keys = fd.keys()
        keys.sort(key=lambda x: fd[x])
        for key in keys:
            fp.write(key + ' ' + str(fd[key]) + '\n')


if __name__ == '__main__':
    tokens_fd = FreqDist()
    tokens_doc_fd = FreqDist()

    for doc in mimic_doc_yielder(MIMIC_PATH):
        tokens_set = set()
        for word in doc[1]:
            tokens_fd[word] += 1
            tokens_set.add(word)
        for word in tokens_set:
            tokens_doc_fd[word] += 1

    write_fd_to_file(tokens_fd, 'tokens_count_global')
    write_fd_to_file(tokens_doc_fd, 'tokens_count_doc')
