# -*- coding: utf-8 -*-
"""NLP Basics.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15EwzJbAhMO226lSVAQ9D73zPd8z4aO-A
"""

import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score

df1 = pd.read_csv('https://raw.githubusercontent.com/gtmray/imdb/master/imdb_train.csv')
df2 = pd.read_csv('https://raw.githubusercontent.com/gtmray/imdb/master/imdb_test.csv')
df = df1.append(df2)
df_decreased = df.iloc[:50000, :]
print(df_decreased.shape)
# paragraph = "My 123 name is Rewan Gautam Rewan. I come from the heart of purbanchal, Itahari. It is biggest city of Sunsari district. I am the person you will not predict even with neural networks."
# sentence = nltk.sent_tokenize(paragraph)
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

#Converting sentences to cleaned sentences with 
# - lowercase
# - taking only alphabets
# - lemmatization

import re
stop = stopwords.words('english')
cleaned = []
sentence = df_decreased['text']
for i in sentence:
  i = re.sub('[^a-zA-Z]', ' ', i)
  i = i.lower()
  words = nltk.word_tokenize(i)
  temp = [stemmer.stem(word) for word in words if word not in stop]
  cleaned.append(" ".join(temp))

#Bag of Words Model
#  - rows = sentences
#  - columns = words

cleaned = df_decreased['text']
from sklearn.feature_extraction.text import CountVectorizer #Count of words in each sentence
cv = CountVectorizer(max_features=5000, stop_words='english')
X = cv.fit_transform(cleaned).toarray()

#Bag of words is not good as tfidf because it has no semantic meaning but perform well in sentiment analysis

'''
Term Frequency(tf) = No. of repeated word in sentence / No. of words in sentence
Inverse Document Frequency(idf) = log(No. of sentences/No. of sentence containing words)
tfidf = tf*idf
'''

from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer(max_features=10000, stop_words='english')
X_tfidf = tfidf.fit_transform(cleaned).toarray()

X_train, X_test, y_train, y_test = train_test_split(X_tfidf, df_decreased.label, test_size=0.2, random_state=42)

model = MultinomialNB()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print(confusion_matrix(y_pred, y_test))
print(accuracy_score(y_pred, y_test))
print(classification_report(y_pred, y_test))

"""<h1>*******Using Word2Vec*******<h1>"""

######## Word2Vec ##########
'''
In both bag of words and tfidf, semantic information  is not stored. 
TF-IDF gives importance to uncommon words.
Chance of over fitting.

- The solution is Word2Vec. Here, each word is represented as a vector of 32 or
more dimension instead of a single number.
- Here the semantic information and relation between different words is also
preserved
'''

import re
from gensim.models import Word2Vec
paragraph = "My 123 name is Rewan Gautam Rewan. I come from the heart of purbanchal, Itahari. It is biggest city of Sunsari district. I am the person you will not predict even with neural networks."

#Data proprocessing

text = re.sub(r'\[[0-9]*\]', ' ', paragraph)
text = re.sub(r'\s+', ' ', text)
text = text.lower()
text = re.sub(r'\d', ' ', text)
text = re.sub(r'\s+', ' ', text)

sentences = nltk.sent_tokenize(text)
sentences = [nltk.word_tokenize(sentence) for sentence in sentences]

for i in range(len(sentences)):
  sentences[i] = [word for word in sentences[i] if word not in stopwords.words('english')]

#Training Word2Vec model

model = Word2Vec(sentences, min_count=1)
words = model.wv.vocab
vector = model.wv['rewan']
similar = model.wv.most_similar('rewan')
print(similar)

"""<h1>Fake news classifier</h1>"""

# ! pip install -q kaggle
# from google.colab import files
# files.upload()
# ! mkdir ~/.kaggle 
# ! cp kaggle.json ~/.kaggle/
# ! chmod 600 ~/.kaggle/kaggle.json
# ! kaggle datasets list
# ! kaggle competitions download -c fake-news
# !unzip train.csv.zip
# !unzip test.csv.zip

import numpy as np
import pandas as pd

df = pd.read_csv('/content/train.csv')
print(df.columns)
df = df.dropna()
df.drop('id', axis=1, inplace=True)
df['text_new'] = df['title']

cleaned = df['text_new']

from sklearn.feature_extraction.text import CountVectorizer #Count of words in each sentence
cv = CountVectorizer(max_features=5000, stop_words='english')
X = cv.fit_transform(cleaned).toarray()

# from sklearn.feature_extraction.text import TfidfVectorizer
# tfidf = TfidfVectorizer(max_features=10000, stop_words='english')
# X_tfidf = tfidf.fit_transform(cleaned).toarray()

X_train, X_test, y_train, y_test = train_test_split(X, df.label, test_size=0.2, random_state=42)
#print(X_test.shape)
model = MultinomialNB()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print(confusion_matrix(y_pred, y_test))
print(accuracy_score(y_pred, y_test))
print(classification_report(y_pred, y_test))





"""<h1>Fake News Classifier using deep learning with LSTM</h1>"""

# ! pip install -q kaggle
# from google.colab import files
# files.upload()
# ! mkdir ~/.kaggle 
# ! cp kaggle.json ~/.kaggle/
# ! chmod 600 ~/.kaggle/kaggle.json
# ! kaggle datasets list
# ! kaggle competitions download -c fake-news
# !unzip train.csv.zip
# !unzip test.csv.zip

import numpy as np
import pandas as pd

df = pd.read_csv('/content/train.csv')
df = df.dropna()
X = df.drop('label', axis=1)
y = df['label']

import tensorflow as tf
from tensorflow.keras.preprocessing.text import one_hot
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam, SGD

import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
nltk.download('stopwords')

#Preprocessing

text = X.copy()
text.reset_index(inplace=True)

corpus = []
ps = PorterStemmer()

for i in range(0, len(text)):
  cleaning = re.sub('[^a-zA-Z]', ' ', text['title'][i])
  cleaning = cleaning.lower()
  cleaning = cleaning.split()

  cleaning = [ps.stem(word) for word in cleaning if not word in stopwords.words('english')]
  cleaning = " ".join(cleaning)
  corpus.append(cleaning)

voc_size = 5000 #Number of words for the one hot encoding
sent_length = 20 #Max length for padding
embedding_vector_features = 40 #Number of vector features for embedding

#One hot encoding
onehot_repr = [one_hot(sentence, voc_size) for sentence in corpus]

#Padding
embedded_docs = pad_sequences(onehot_repr, padding='pre', maxlen=sent_length)

#Model

model = Sequential()
model.add(Embedding(voc_size, embedding_vector_features, input_length=sent_length))
model.add(Dropout(0.4))

model.add(LSTM(100, return_sequences=True))
model.add(BatchNormalization())
model.add(Dropout(0.4))

model.add(LSTM(100, return_sequences=True))
model.add(BatchNormalization())
model.add(Dropout(0.4))

model.add(LSTM(100))
model.add(BatchNormalization())
model.add(Dropout(0.4))

model.add(Dense(1, activation='sigmoid'))

model.summary()

#Compile model
model.compile(loss='binary_crossentropy', optimizer=Adam(learning_rate=0.01), metrics=['accuracy'])

#Converting to numpy array

X_final = np.array(embedded_docs)

y_final = np.array(y)

#Splitting dataset to training and testing 

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X_final, y_final, test_size=0.2, random_state=77)

#Model training

model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=20, batch_size=100)

#Model performance

from sklearn.metrics import confusion_matrix, accuracy_score
y_pred = model.predict_classes(X_test)
print(confusion_matrix(y_test, y_pred))
print(accuracy_score(y_test, y_pred))

def preprocessing_and_all(dataframe_dir):
  df_test = pd.read_csv(dataframe_dir)
  df_temp = df_test.copy()
  df_temp['text'] = df_temp['text'].str[:10]
  df_temp['title'] = df_temp['title'].fillna(df_temp['text'])
  df_temp.reset_index(inplace=True)

  corpus = []
  ps = PorterStemmer()

  for i in range(0, len(df_temp)):
    cleaning = re.sub('[^a-zA-Z]', ' ', df_temp['title'][i])
    cleaning = cleaning.lower()
    cleaning = cleaning.split()

    cleaning = [ps.stem(word) for word in cleaning if not word in stopwords.words('english')]
    cleaning = " ".join(cleaning)
    corpus.append(cleaning)
  
  voc_size = 5000 #Number of words for the one hot encoding
  sent_length = 20 #Max length for padding
  embedding_vector_features = 40 #Number of vector features for embedding

  #One hot encoding
  onehot_repr = [one_hot(sentence, voc_size) for sentence in corpus]

  #Padding
  embedded_docs = pad_sequences(onehot_repr, padding='pre', maxlen=sent_length)
  
  X = np.array(embedded_docs)
  y_pred_real = model.predict_classes(X)  
  df_temp['label'] = y_pred_real
  df_to_submit = df_temp[['id', 'label']]
  return df_to_submit

df_sum = preprocessing_and_all('/content/test.csv')
print(df_sum.head())
print(df_sum.info())
df_sum.to_csv('/content/final.csv', index=False)
!kaggle competitions submit fake-news -f /content/final.csv -m "My submission message"









