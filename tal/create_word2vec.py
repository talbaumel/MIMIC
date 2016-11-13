from gensim.models import Word2Vec
from token_analsys import mimic_doc_yielder

MIMIC_PATHS = ['../../MIMIC2/MIMIC_PREPROCESSED', '../../MIMIC3/MIMIC_PREPROCESSED']

sentences = []
codes = []
for path in MIMIC_PATHS:
    for code, text in mimic_doc_yielder(path):
        sentences.append(text)
        codes.append(code)

model = Word2Vec(codes, size=100, window=250, min_count=5, workers=4)
model.save('mimic_codes_w2v100')
print 'hi!'
model = Word2Vec(codes, size=50, window=250, min_count=5, workers=4)
model.save('mimic_codes_w2v50')
print 'hi!'
model = Word2Vec(sentences, size=200, window=5, min_count=5, workers=4)
model.save('mimic_text_w2v100')
print 'hi!'
model = Word2Vec(sentences, size=100, window=5, min_count=5, workers=4)
model.save('mimic_text_w2v50')
print 'hi!'