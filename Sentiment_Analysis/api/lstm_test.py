#! /bin/env python
# -*- coding: utf-8 -*-
"""
预测
"""

import os
os.environ['KERAS_BACKEND']='theano'
import jieba
import numpy as np
from gensim.models.word2vec import Word2Vec
from gensim.corpora.dictionary import Dictionary
from keras.preprocessing import sequence

import yaml
from keras.models import model_from_yaml

np.random.seed(1337)  # For Reproducibility
import sys

sys.setrecursionlimit(1000000)

# define parameters
maxlen = 100


def create_dictionaries(model=None,
                        combined=None):
    ''' Function does are number of Jobs:
        1- Creates a word to index mapping
        2- Creates a word to vector mapping
        3- Transforms the Training and Testing Dictionaries

    '''
    if (combined is not None) and (model is not None):
        gensim_dict = Dictionary()
        gensim_dict.doc2bow(model.wv.vocab.keys(),
                            allow_update=True)
        #  freqxiao10->0 所以k+1
        w2indx = {v: k + 1 for k, v in gensim_dict.items()}  # 所有频数超过10的词语的索引,(k->v)=>(v->k)
        w2vec = {word: model[word] for word in w2indx.keys()}  # 所有频数超过10的词语的词向量, (word->model(word))

        def parse_dataset(combined):  # 闭包-->临时使用
            ''' Words become integers
            '''
            data = []
            for sentence in combined:
                new_txt = []
                for word in sentence:
                    try:
                        new_txt.append(w2indx[word])
                    except:
                        new_txt.append(0)  # freqxiao10->0
                data.append(new_txt)
            return data  # word=>index

        combined = parse_dataset(combined)
        combined = sequence.pad_sequences(combined, maxlen=maxlen)  # 每个句子所含词语对应的索引，所以句子中含有频数小于10的词语，索引为0
        return w2indx, w2vec, combined
    else:
        print('No data provided...')


def input_transform(string):
    words = jieba.lcut(string)
    words = np.array(words).reshape(1, -1)
    module_path = os.path.dirname(__file__)
    filename = module_path + '/model/Word2vec_model.pkl'
    model = Word2Vec.load(filename)
    _, _, combined = create_dictionaries(model, words)
    return combined


def lstm_predict(text):
    print('loading model......')
    module_path = os.path.dirname(__file__)
    filename = module_path + '/model/lstm.yml'
    with open(filename, 'r') as f:
        yaml_string = yaml.load(f, Loader=yaml.FullLoader)
    model = model_from_yaml(yaml_string)

    print('loading weights......')
    filename = module_path + '/model/lstm.h5'
    model.load_weights(filename)
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam', metrics=['accuracy'])

    msg = ""
    lines = text.split("\n")
    for line in lines:
        print(line)
        data = input_transform(line)
        data.reshape(1, -1)
        result = model.predict_classes(data)
        if result[0] == 1:
            msg += "positive\n"
        elif result[0] == 0:
            msg += "neural\n"
        else:
            msg += "negative\n"
    return msg


if __name__ == '__main__':
    theano.test()
    lists = "酒店的环境非常好，价格也便宜，值得推荐。\n手机质量太差了，傻逼店家，赚黑心钱，以后再也不会买了。\n总体来说不好，文字、内容、结构都不好。\n虽说是职场指导书，但是写的有点干涩，我读一半就看不下去了！书的质量还好，但是内容实在没意思。\n本以为会侧重心理方面的分析，但实际上是婚外恋内容。\n不好。\n真的一般，没什么可以学习的。"
    #lists = "哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈毕业季出来挨打"
    msg = lstm_predict(lists)
    print(msg)
