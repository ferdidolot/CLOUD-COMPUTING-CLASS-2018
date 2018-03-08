import nltk
nltk.download('punkt') 
import re

from collections import Counter

def get_tokens():
    with open('FirstContactWithTensorFlow.txt', 'r') as tf:
        text = tf.read()
        lowers = text.lower()
        no_punctuation = re.sub(r'[^\w\s]','',lowers)
        tokens = nltk.word_tokenize(no_punctuation)
    return tokens

tokens = get_tokens()
count = Counter(tokens)
print (count.most_common(10))
print('The total number of the words of the book after removing punctuation is:', len(tokens))
