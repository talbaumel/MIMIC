from token_analsys import mimic_doc_yielder
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer

MIMIC_PATH = '../../MIMIC2/MIMIC_PREPROCESSED'
CODE_ROUTE = '../../MIMIC2/all_mimic2_codes_with_route'
CODES = '../../MIMIC2/all_mimic2_codes'

code_to_route = {}
for line in open(CODE_ROUTE):
    line = line.strip().split()
    code_to_route[line[0]] = line[1].split(',')



class MIMIC_Reader:

    def _create_target_for_codes(self, codes, categories):
        return MultiLabelBinarizer().fit_transform( codes)#see how to pass class number

    def __init__(self, mimic_file, categories, is_train=True):
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
            # if not self._should_include(codes, label):
            #     if is_train:
            #         continue
            data = (' '.join(words)).decode('utf-8')
            self.data.append(data)
            self.target.append(self._create_target_for_codes(codes[0], categories))
            #self.target.append(label in codes)

        self.target = np.asarray(self.target)
        self.target_names = categories# code_to_route.keys()#['in', 'out']


if __name__ == '__main__':
    data = MIMIC_Reader(MIMIC_PATH, '250.00', False)
    print data.target.shape
    print sum(data.target)




