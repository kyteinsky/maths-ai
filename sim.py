import gzip
import gensim
from multiprocessing import cpu_count
import argparse
import os

ap = argparse.ArgumentParser()
ap.add_argument('--train', action='store_true', help='True or Flase to train')
ap.add_argument('--ds', type=str, help='dataset file name with location', required=True)
ap.add_argument('-a', type=str)
ap.add_argument('-b', type=str)
ap.add_argument('-c', type=str)
args = vars(ap.parse_args())
tr = args['train']

data_file = args['ds']
saved_model_path = 'savedmodel/maths-ai-model'

def train():
    print('reading file ..')
    def read_file(file):
        with gzip.open(file, 'rb') as f:
            for line in f:
                yield gensim.utils.simple_preprocess(line)


    data = list(read_file(data_file))
    print('creating model ..')
    model = gensim.models.Word2Vec(data, size=150, window=10, min_count=2, workers=cpu_count())
    if os.path.isfile(saved_model_path):
        model = gensim.models.Word2Vec.load(saved_model_path)
    print('starting training ..')
    model.train(data,total_examples=len(data),epochs=10)
    model.save(saved_model_path)
    print('done')


def demo(a, b, c): # a + b - c -- actually a + c - b
    model = gensim.models.Word2Vec.load(saved_model_path)
    try:
        return model.wv.most_similar_cosmul(positive=[a, c], negative=[b])[0][0]
    except:
        return 'Word not in my dictionary, sorry.'

if __name__ == '__main__':
    if tr: train()
    else: print(demo(args['a'], args['b'], args['c']))
