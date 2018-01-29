path = '/tal_files/attention_classifier/mimic/'
mimic_file = path+'MIMIC_PREPROCESSED2'
mimic_shaped = path+'shaped_mimic2'
ICD9_DESCRIPTIONS = path+'ICD9_descriptions'
CODE_ROUTE = path+'all_codes_with_route'
word2vec_code_file = path+'mimic_codes_w2v50'
split_size = 20533 #49857


from gensim.models import Word2Vec
from sklearn.cluster import KMeans
from collections import defaultdict
import re
from nltk.corpus import stopwords
labels_vocab = set()
tokens_vocab = set()
tokens_to_int = {}


def get_all_labels():
    global labels_vocab
    all_labels = []
    for line in open(mimic_file, errors='ignore'):
        labels = line.split('|')[0].split(',')
        labels_vocab |= set(labels)
        all_labels.append(labels)
    return all_labels

sw = stopwords.words('english')
def get_all_tokens():
    global tokens_vocab
    all_tokens = []
    for line in open(mimic_shaped, errors='ignore'):
        tokens = line.strip().split()
        tokens_vocab |= set(tokens)
        all_tokens.append(tokens)
    tokens_vocab = list(tokens_vocab)
    for i, token in enumerate(tokens_vocab):
        tokens_to_int[token] = i
    return all_tokens


def to_int(lists, d):
    return [[d[i] for i in l] for l in lists]


def create_w2v_clusters():
    w2v = Word2Vec.load(word2vec_code_file)
    word_vec = []
    for word in w2v.vocab:
        word_vec.append((word, w2v[word]))

    def cluster(words_vectors):
        vectors = [wv[1] for wv in words_vectors]
        clusterer = KMeans(n_clusters=2, init='k-means++')
        clusterer.fit(vectors)
        labels = clusterer.predict(vectors)
        clusters = defaultdict(list)
        for label, vector in zip(labels, words_vectors):
            clusters[label].append(vector)
        return clusters

    def hier_cluster(word_vec, max_cluster=200):
        clusters = cluster(word_vec)
        tree = []
        for label in clusters:
            if len(clusters[label]) < max_cluster:
                tree.append(clusters[label])
            else:
                tree.append(hier_cluster(clusters[label], max_cluster=max_cluster))
        return tree

    tree = hier_cluster(word_vec)

    clusters = []
    def get_clusters(tree):
        for node in tree:
            if type(node[0]) == list:
                get_clusters(node)
            else:
                clusters.append([x[0] for x in node])
    get_clusters(tree)
    singeltons = []
    singeltons_index = []
    for i, c in enumerate(clusters):
        if len(c) == 1:
            singeltons += c
            singeltons_index.append(i-len(singeltons_index))
    for i in singeltons_index:
        clusters.pop(i)
    clusters.append(singeltons)
    return clusters

def read_mimic():
    x = to_int(get_all_tokens(), tokens_to_int)
    y = get_all_labels()

    clusters = create_w2v_clusters()
    label_to_cluster_num = {}
    for i, c in enumerate(clusters):
        for l in c:
            label_to_cluster_num[l] = i

    label_to_int = {}
    for cluster in clusters:
        for i, label in enumerate(cluster):
            label_to_int[label] = i

    cluster_ys = []
    for i in range(len(clusters)):
        cluster_ys.append([])
        for example in y:
            cluster_ys[-1].append([])
            for label in example:
                if i == label_to_cluster_num[label]:
                    cluster_ys[-1][-1].append(label)
    ys_int = []
    for y in cluster_ys:
        ys_int.append(to_int(y, label_to_int))

    x_train, x_test = x[:split_size], x[split_size:]
    y_trains, y_tests = [c[:split_size] for c in ys_int], [c[split_size:] for c in ys_int]

    return x_train, x_test, y_trains, y_tests, tokens_vocab, clusters

if __name__ == '__main__':
    read_mimic()