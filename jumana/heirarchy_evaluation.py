from collections import defaultdict
from code2route import create_child2parent_tree,find_route

ICD_TREE_FILE = './data/ICD9_parent_child_relations'
'''
 true positives were defined as predicted codes that were ancestors of, descendants of, or identical to a gold-standard code.
 False positives were defined as predicted codes that are not true positives.
 False negatives were defined as gold-standard codes where the code itself or a descendant was not predicted.'''
def heirarchy_f(predictions, golds):
    child2parent = create_child2parent_tree(ICD_TREE_FILE)

    TPc = defaultdict(int)
    FPc = defaultdict(int)
    FNc = defaultdict(int)
    labels = set()
    for prediction, gold in zip(predictions, golds):
        for label in prediction:
            labels.add(label)
            if label in gold:
                TPc[label] += 1
            else:
                FPc[label] += 1
        for label in gold:
            labels.add(label)
            if not label in prediction:
                FNc[label] += 1
    Pc = defaultdict(float)
    Rc = defaultdict(float)
    for label in labels:
        if (TPc[label] + FPc[label]) > 0:
            Pc[label] = TPc[label] / float(TPc[label]+FPc[label])
        if (TPc[label]+FNc[label]) > 0:
            Rc[label] = TPc[label] / float(TPc[label]+FNc[label])

    macrof = 0
    for label in labels:
        if (Pc[label]+Rc[label]) > 0:
            macrof += (2*Pc[label]*Rc[label]) / (Pc[label]+Rc[label])
    return macrof/len(labels)


if __name__ == '__main__':
    predictions = [['good', 'bad'], ['good', 'yellow']]
    golds = [['good', 'bad'], ['good', 'red']]


    print macro_f(predictions, golds)