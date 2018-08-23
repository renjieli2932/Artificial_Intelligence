# Artifical Intelligence @ edX
# Week11 Project
# Natural Language Processing
# Renjie Li, rl2932@columbia.edu
import pandas  # pandas.read_csv(filename,encoding="ISO-8859-1")
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer # TfidfVectorizer seems to be combination of the above two , so actually I didnot use the above one
from sklearn.linear_model import SGDClassifier # loss="hinge" penalty="l1"
import os
import string


class IMDB(object):

    def __init__(self):
        #self.train_path = "../resource/lib/publicdata/aclImdb/train/" # use terminal to ls files under this directory
        #self.test_path = "../resource/asnlib/public/imdb_te.csv" # test data for grade evaluation
        self.train_path = "aclImdb/train/"
        self.test_path = "test.csv"
        self.num = 0 # used to number the train data
        self.stopwordprocessing()
        #self.imdb_data_preprocess()
        self.train_data = pandas.read_csv("imdb_tr.csv")
        self.test_data = pandas.read_csv(self.test_path,encoding="ISO-8859-1")

        self.Unigram()
        self.Bigram()
        self.Unigram_Tfidf()
        self.Bigram_Tfidf()

    def Unigram(self):
        self.countvector = CountVectorizer(stop_words=self.stopwords)
        self.train_trans = self.countvector.fit_transform(self.train_data['text'])
        self.SGD = SGDClassifier(loss='hinge',penalty='l1')
        self.SGD.fit(self.train_trans,self.train_data['polarity'])

        self.test_trans = self.countvector.transform(self.test_data['text'])
        unigram = self.SGD.predict(self.test_trans)
        with open("unigram.output.txt",'w') as f:
            for item in unigram:
                f.write(str(item)+'\n')

    def Bigram(self):
        self.countvector = CountVectorizer(stop_words=self.stopwords,ngram_range=(1,2))
        self.train_trans = self.countvector.fit_transform(self.train_data['text'])
        self.SGD = SGDClassifier(loss='hinge', penalty='l1')
        self.SGD.fit(self.train_trans, self.train_data['polarity'])

        self.test_trans = self.countvector.transform(self.test_data['text'])
        bigram = self.SGD.predict(self.test_trans)
        with open("bigram.output.txt", 'w') as f:
            for item in bigram:
                f.write(str(item) + '\n')


    def Unigram_Tfidf(self):
        self.countvector = TfidfVectorizer(stop_words=self.stopwords)
        self.train_trans = self.countvector.fit_transform(self.train_data['text'])
        self.SGD = SGDClassifier(loss='hinge', penalty='l1')
        self.SGD.fit(self.train_trans, self.train_data['polarity'])

        self.test_trans = self.countvector.transform(self.test_data['text'])
        unigram = self.SGD.predict(self.test_trans)
        with open("unigramtfidf.output.txt", 'w') as f:
            for item in unigram:
                f.write(str(item) + '\n')



    def Bigram_Tfidf(self):
        self.countvector = TfidfVectorizer(stop_words=self.stopwords, ngram_range=(1, 2))
        self.train_trans = self.countvector.fit_transform(self.train_data['text'])
        self.SGD = SGDClassifier(loss='hinge', penalty='l1')
        self.SGD.fit(self.train_trans, self.train_data['polarity'])

        self.test_trans = self.countvector.transform(self.test_data['text'])
        bigram = self.SGD.predict(self.test_trans)
        with open("bigramtfidf.output.txt", 'w') as f:
            for item in bigram:
                f.write(str(item) + '\n')




    def stopwordprocessing(self):
        with open("stopwords.en.txt") as f:
            self.stopwords = f.read()
        self.stopwords = self.stopwords.split('\n')
        if self.stopwords[-1] == '': # It's weird that I find '' in the last line
            self.stopwords.pop(-1)
        #print(self.stopwords)

    def imdb_data_preprocess(self,outpath="./", name="imdb_tr.csv", mix=False):
        self.f = open(name, 'w')
        self.f.write("row_number,text,polarity\n")  # Header
        self.imdbtr(name, 'pos', '1')
        self.imdbtr(name, 'neg', '0')
        self.f.close()

    def imdbtr(self,name, folder, polarity):
        realpath = self.train_path + folder
        for item in os.listdir(realpath):
            with open(realpath + '/' + item) as f_content:
                content = self.content_processing(f_content.read())
                #content = f_content.read()
            self.f.write(str(self.num) + ',' + content + ',' + str(polarity) + '\n')
            self.num += 1

    def content_processing(self,content):
        '''
        Comma is annoying in text, as well as '<br>' .idk what is that...
        '''
        text = content
        text = text.replace("<br />",'') # <br /> seems to be a symbol for line breaking
        #text = text.replace(",", ' ')
        #text = text.replace(".", ' ')
        #text = text.replace("'", ' ')
        translator = string.maketrans(string.punctuation,' '*len(string.punctuation)) # credit to stackoverflow
        text = text.translate(translator)
        text = text.lower() # Stopwords are all in lower-case...
        splittext =text.split()
        realtext = ''
        for word in splittext:
            if word not in self.stopwords:
                realtext += word + ' '
        return realtext



if __name__ == "__main__":
    imdb = IMDB()
