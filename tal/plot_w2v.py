from gensim.models import Word2Vec
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from sklearn.manifold import TSNE


def main():
    embeddings_file = "mimic_text_w2v100"
    wv, vocabulary = load_embeddings(embeddings_file)

    tsne = TSNE(n_components=2, random_state=0)
    np.set_printoptions(suppress=True)
    Y = tsne.fit_transform(wv[100:200])

    plt.scatter(Y[:, 0], Y[:, 1])
    for label, x, y in zip(vocabulary, Y[:, 0], Y[:, 1]):
        plt.annotate(label, xy=(x, y), xytext=(0, 0), textcoords='offset points')
    plt.show()

def get_sort_key_dict():
    path1 = '../../MIMIC2/stats/tokens_count_global'
    path2 = '../../MIMIC3/stats/tokens_count_global'
    code_to_count = defaultdict(int)
    for path in [path1, path2]:
        for line in open(path):
            line = line.strip().split()
            code_to_count[line[0]] += int(line[1])
    return code_to_count


def load_embeddings(file_name):
    model = Word2Vec.load(file_name)
    sort_key_dict = get_sort_key_dict()
    vocab = model.vocab
    vocab = sorted(vocab, key=lambda x:sort_key_dict[x], reverse=True)
    return zip(*map(lambda x: (model[x], x), vocab))



if __name__ == '__main__':
    main()