from sklearn.feature_extraction.text import TfidfVectorizer
from optparse import OptionParser
from MIMIC_reader import MIMIC_Reader

op = OptionParser()
op.add_option("--category_list",
              action="store" , type="str", dest="category_list",
              help="A file including categories to include, each category in a new line.")
op.add_option("--corpus_path",
              action="store" , type="str", dest="corpus_path", default='../../MIMIC2/MIMIC_PREPROCESSED',
              help="Path to the corpus file.")

data_train = MIMIC_Reader(opts.corpus_path, categories, True)
vectorizer = TfidfVectorizer(sublinear_tf=True, max_features=10000, #min_df=0.00009 , max_df=0.5,
                                 stop_words='english', ngram_range = (1,3))
    X_train = vectorizer.fit_transform(data_train.data)
