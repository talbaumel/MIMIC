from token_analsys import mimic_doc_yielder
import numpy as np
MIMIC_PATH = '../../MIMIC2/MIMIC_PREPROCESSED'
CODE_ROUTE = '../../MIMIC2/all_mimic2_codes_with_route'

code_to_route = {}
for line in open(CODE_ROUTE):
    line = line.strip().split()
    code_to_route[line[0]] = line[1].split(',')

class MIMIC_Reader:
    def _should_include(self, codes, label):
        label_route = '_'.join(code_to_route[label][:-1])
        for code in codes:
            if label_route == '_'.join(code_to_route[code][:-1]):
                return True
        return False

    def _is_positeve(self, codes, label):
        label_route = '_'.join(code_to_route[label])
        for code in codes:
            code_label = '_'.join(code_to_route[code])
            if code_label.startswith(label_route):
                return 1
            if label_route.startswith(code_label):
                return 1
        return 0

    def __init__(self, mimic_file, label, is_train=True):
        all = []
        for doc in mimic_doc_yielder(mimic_file):
            all.append(doc)
        self.data = []
        self.target = []
        if is_train:
            all = all[:int(len(all)*0.9)]
        else:
            all = all[int(len(all)*0.9):]
        for doc in all:
            codes, words = doc[0], doc[1]
            if not self._should_include(codes, label):
                if is_train:
                    continue
            data = (' '.join(words)).decode('utf-8')
            self.data.append(data)
            self.target.append(self._is_positeve(codes, label))
        self.target = np.asarray(self.target)
        self.target_names = ['out', 'in']

if __name__ == '__main__':
    data = MIMIC_Reader(MIMIC_PATH, '250.00', False)
    print data.target.shape
    print sum(data.target)




