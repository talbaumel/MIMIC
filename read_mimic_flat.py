from codecs import open
from numpy import nanmean, where, array, float, zeros


class mimic_reader:
    def __init__(self, version, expand=True, shaped=True, add_desc=False, generlize=False):
        self.v = version
        self.add_desc = add_desc
        self.expand = expand
        self.shaped = shaped
        self.generlize = generlize
        self.code_to_route = {}
        for line in open('mimic/' + version + '/all_codes_with_route'):
            line = line.strip().split()
            code = line[0]
            route = line[1].split(',')
            self.code_to_route[code] = route

    def _add_ancestors(self, labels):
        labels_anc = []
        for label in labels:
            if label in self.code_to_route:
                labels_anc += self.code_to_route[label]
            else:
                print('didn\'t find ancestors for: ' + label)
            labels_anc.append(label)
        return labels_anc

    def _to_int(self, corpus):
        vocab = set()
        for doc in corpus:
            for word in doc:
                vocab.add(word)

        to_int = {w: i for i, w in enumerate(vocab)}
        int_corpus = []
        for doc in corpus:
            int_corpus.append([to_int[w] for w in doc if w in vocab])
        vocab = list(vocab)
        return int_corpus, vocab, to_int

    def _split(self):
        if self.v == '2':
            return 20533
        if self.v == '3':
            return 49857

    def read_desc(self, words_vocab, labels_vocab):
        labels = []
        words = []
        for line in open('mimic/' + self.v + '/ICD9_descriptions'):
            line = line.strip().split('\t')
            if line[0] in labels_vocab:
                labels.append(self._add_ancestors([line[0]]))
                words.append(filter(lambda w: w in words_vocab, line[1].split()))
        return words, labels

    def read_mimic(self):
        Xs, Ys, Ys_anc = [], [], []
        if self.shaped:
            path = 'mimic/' + self.v + '/MIMIC_FILTERED_DSUMS'
        else:
            path = 'mimic/' + self.v + '/MIMIC_PREPROCESSED'

        for line in open(path, encoding='utf-8'):
            line = line.strip().split('|')
            labels = line[0].split(',')
            if self.generlize:
                labels = [label.split('.')[0] for label in labels]
            labels_anc = self._add_ancestors(labels)
            words = line[1].split()
            
            #words = [w for w in words  if len(w) > 2 ]
            
            Xs.append(words)
            Ys.append(labels)
            Ys_anc.append(labels_anc)
        self.gold = [self.only_leaves(codes) for codes in Ys[self._split():]]
        #self.gold = [set(codes) for codes in Ys[self._split():]]
        if self.expand:
            Ys = Ys_anc
        Xs, words_vocab, word2int = self._to_int(Xs)
        X_train, X_test = Xs[:self._split()], Xs[self._split():]
        Ys, labels_vocab, label2int = self._to_int(Ys)
        Y_train, Y_test = Ys[:self._split()], Ys[self._split():]

        if self.add_desc:
            words, labels = self.read_desc(words_vocab, labels_vocab)
            int_words = []
            for doc in words:
                int_words.append([word2int[w] for w in doc])
            int_labels = []
            for doc in labels:
                int_labels.append([label2int[l] for l in doc])
            X_train += int_words
            Y_train += int_labels

        return X_train, X_test, Y_train, Y_test, words_vocab, labels_vocab

    def _eval_non_hier(self, y_true, y_pred):
        TPs = []
        FPs = []
        FNs = []

        for true, pred in zip(y_true, y_pred):
            true = set(true)
            pred = set(pred)
            tp = len(pred.intersection(true))
            fp = len(pred - true)
            fn = len(true - pred)
            TPs.append(tp), FPs.append(fp), FNs.append(fn)
        FNs = array(FNs, float)
        FPs = array(FPs, float)
        TPs = array(TPs, float)
        return TPs, FPs, FNs

    def _eval_hier(self, y_true, y_pred):
        TPs = []
        FPs = []
        FNs = []

        for true, pred in zip(y_true, y_pred):
            tp, fp, fn = 0, 0, 0
            true_anc = set(self._add_ancestors(true))
            pred_anc = set(self._add_ancestors(pred))
            true = set(true)
            pred = set(pred)
            for label in pred:
                if label in true or label in true_anc or set(self.code_to_route[label]).intersection(true):
                    tp += 1
                else:
                    fp += 1
            for code in true:
                if len(set(self.code_to_route[code]) - pred_anc) > 0:
                    fn += 1
            TPs.append(tp), FPs.append(fp), FNs.append(fn)
        FNs = array(FNs, float)
        FPs = array(FPs, float)
        TPs = array(TPs, float)
        return TPs, FPs, FNs

    def _eval(self, y_true, is_hier):
        if is_hier:
            TPs, FPs, FNs = self._eval_hier(self.gold, y_true)
        else:
            TPs, FPs, FNs = self._eval_non_hier(self.gold, y_true)

        prec = nanmean(where(TPs + FPs > 0, TPs / (TPs + FPs), 0))

        rec = nanmean(where(TPs + FNs > 0, TPs / (TPs + FNs), 0))
        if not rec + prec == 0:
            f = 2 * (rec * prec) / (rec + prec)
        else:
            f = 0
        return rec, prec, f

    def only_leaves(self, codes):
        leaves = []
        all_ancestors = set()
        for code in codes:
            all_ancestors |= set(self.code_to_route[code][:-1])
        for code in codes:
            if code not in all_ancestors:
                leaves.append(code)
        return leaves

    def evaluate(self, pred):
        pred = [self.only_leaves(codes) for codes in pred]
        #pred = [set(codes) for codes in pred]
        hier = self._eval(pred, is_hier=True)
        non_hier = self._eval(pred, is_hier=False)
        return {'hier': hier, 'non_hier': non_hier}




if __name__ == '__main__':
    version = '2'
    expand = False
    shaped = True
    add_desc = False
    min_count = 1
    
    reader = mimic_reader(version, expand=expand, shaped=shaped, add_desc=add_desc)
    X_train, X_test, y_trains, y_test, tokens_vocab, labels_vocab = reader.read_mimic()

    t = []
    for _ in y_test:
        t.append(['@'])
    print(reader.evaluate(t))


    icd_preds = []

    for pred in y_test:
        labels = []
        for p in pred:
            labels.append(labels_vocab[p])
        icd_preds.append(labels)

    print(reader.evaluate(icd_preds))