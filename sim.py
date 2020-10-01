import gzip
from gensim.models import KeyedVectors
from multiprocessing import cpu_count
import argparse
import os


ap = argparse.ArgumentParser()
ap.add_argument('--train', action='store_true', help='True or Flase to train')
ap.add_argument('-a', type=str)
ap.add_argument('-b', type=str)
ap.add_argument('-c', type=str)
args = vars(ap.parse_args())
tr = args['train']

saved_model_path = 'savedmodel/glove.6B.50d.txt'



def train():
    # if not os.path.isfile(saved_model_path):
    model = api.load('glove-twitter-50')
    # model = gensim.models.Word2Vec(saved_model_path)
    print(model.most_similar("cat"))
    print('done')


def demo(a, b, c): # a - b + c
    model = KeyedVectors.load_word2vec_format('savedmodel/GoogleNews-vectors-negative300.bin', binary=True)
    try:
        return model.most_similar_cosmul(positive=[a, c], negative=[b])[0][0]
    except: # Exception as e:
        # return e
        return 'Word not in my dictionary, sorry.'


if __name__ == '__main__':
    if tr: train()
    else: print(demo(args['a'], args['b'], args['c']))

