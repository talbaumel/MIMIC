import numpy as np
from sklearn.metrics import precision_recall_fscore_support, average_precision_score, \
    roc_auc_score, precision_score, recall_score


thres = 0.5

def f1_score(probs, labels, thres, average='micro'):
    '''Returns (precision, recall, F1 score) from a batch of predictions (thresholded probabilities)
       given a batch of labels (for macro-averaging across batches)'''
    preds = (probs >= thres).astype(np.int32)
    p, r, f, _ = precision_recall_fscore_support(labels, preds, average=average,
                                                                 warn_for=())
    return p, r, f

def auc_pr(probs, labels, average='micro'):
    '''Precision integrated over all thresholds (area under the precision-recall curve)'''
    if average == 'macro' or average is None:
        sums = labels.sum(0)
        nz_indices = np.logical_and(sums != labels.shape[0], sums != 0)
        probs = probs[:, nz_indices]
        labels = labels[:, nz_indices]
    return average_precision_score(labels, probs, average=average)


def auc_roc(probs, labels, average='micro'):
    '''Area under the ROC curve'''
    if average == 'macro' or average is None:
        sums = labels.sum(0)
        nz_indices = np.logical_and(sums != labels.shape[0], sums != 0)
        probs = probs[:, nz_indices]
        labels = labels[:, nz_indices]
    return roc_auc_score(labels, probs, average=average)


def precision_at_k(probs, labels, k, average='micro'):
    indices = np.argpartition(-probs, k-1, axis=1)[:, :k]
    preds = np.zeros(probs.shape, dtype=np.int)
    preds[np.arange(preds.shape[0])[:, np.newaxis], indices] = 1
    return precision_score(labels, preds, average=average)


def recall_at_k(probs, labels, k, average='micro'):
    indices = np.argpartition(-probs, k-1, axis=1)[:, :k]
    preds = np.zeros(probs.shape, dtype=np.int)
    preds[np.arange(preds.shape[0])[:, np.newaxis], indices] = 1
    return recall_score(labels, preds, average=average)


def full_evaluate(pred, gold, thres=0.5):
    pred = np.array(pred)
    gold = np.array(gold)

    out = 'f1 micro:'+ str(f1_score(pred, gold, thres, average='micro'))+'\n'
    out += 'f1 macro: '+ str(f1_score(pred, gold, thres, average='macro'))+'\n'

    out += 'auc_pr micro: '+str(auc_pr(pred, gold, average='micro'))+'\n'
    out += 'auc_pr macro: '+str(auc_pr(pred, gold, average='macro'))+'\n'

    out += 'auc_roc micro: ' + str(auc_roc(pred, gold, average='micro'))+'\n'
    out += 'auc_roc macro: ' + str(auc_roc(pred, gold, average='macro'))+'\n'

    out += 'precision_at_k 8: ' + str(precision_at_k(pred, gold, 8, average='micro'))+'\n'
    out += 'precision_at_k 40: ' + str(precision_at_k(pred, gold, 40, average='micro'))+'\n'

    out += 'recall_at_k 8: ' + str(recall_at_k(pred, gold, 8, average='micro'))+'\n'
    out += 'recall_at_k 40: ' + str(recall_at_k(pred, gold, 40, average='micro'))+'\n'
    
    return out


if __name__ == '__main__':
    exp1 = [0.3, 0.9]
    exp2 = [0.8, 0.8]
    gold1 = [1, 1]
    gold2 = [0, 0]
    evaluate([exp1, exp2], [gold1, gold2])