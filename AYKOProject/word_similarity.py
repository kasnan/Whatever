# -*- coding: utf-8 -*-

from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from nltk.tokenize import TreebankWordTokenizer

def token_merge(text_list):
    str = ''
    separtor = ' '
    for idx, val in enumerate(text_list):
         str += val + ('' if idx == len(text_list) -1 else separtor)
    return str

def cos_similarity(v1, v2):
    dot_product = np.dot(v1, v2)
    l2_norm = (np.sqrt(sum(np.square(v1))) * np.sqrt(sum(np.square(v2))))
    similarity = dot_product / l2_norm     
    
    return similarity

def similarity_con(original, text):

    tokenizer = TreebankWordTokenizer()

    original_list = tokenizer.tokenize(original)
    text_list = tokenizer.tokenize(text)
    
    original = token_merge(original_list)
    text = token_merge(text_list)

    doc_list = [original,
                text]
    tfidf_vect_simple = TfidfVectorizer()
    feature_vect_simple = tfidf_vect_simple.fit_transform(doc_list)

    # TFidfVectorizer로 transform()한 결과는 Sparse Matrix이므로 Dense Matrix로 변환. 
    feature_vect_dense = feature_vect_simple.todense()

    #첫번째 문장과 두번째 문장의 feature vector  추출
    vect1 = np.array(feature_vect_dense[0]).reshape(-1,)
    vect2 = np.array(feature_vect_dense[1]).reshape(-1,)

    #첫번째 문장과 두번째 문장의 feature vector로 두개 문장의 Cosine 유사도 추출
    similarity_simple = cos_similarity(vect1, vect2)
    print('문장 1, 문장 2 Cosine 유사도: {0:.3f}'.format(similarity_simple))

    return float(similarity_simple)
