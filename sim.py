import gzip
import gensim
from multiprocessing import cpu_count
import argparse
import os
from nltk.corpus import wordnet
import nltk


ap = argparse.ArgumentParser()
ap.add_argument('--train', action='store_true', help='True or Flase to train')
ap.add_argument('-a', type=str)
ap.add_argument('-b', type=str)
ap.add_argument('-c', type=str)
args = vars(ap.parse_args())
tr = args['train']

saved_model_path = 'savedmodel/maths-ai-model'

def train():
    if not os.path.isfile(saved_model_path):
        nltk.download('wordnet')
        print('creating model ..')
        model = gensim.models.Word2Vec(wordnet.sents())
        model.save(saved_model_path)

    print('done')


def demo(a, b, c): # a - b + c
    model = gensim.models.Word2Vec.load(saved_model_path)
    try:
        return model.wv.most_similar_cosmul(positive=[a, c], negative=[b])[0][0]
    except:
        return 'Word not in my dictionary, sorry.'

if __name__ == '__main__':
    if tr: train()
    else: print(demo(args['a'], args['b'], args['c']))
