# build_vocabulary.py : This file implements the building of the word2Vec Model
#                       given the text corpus

# Relevance between a user query q and Question Q
# Authors: Pratik Patel, Swetul Patel
# Created on: 12/2/2020
import multiprocessing

from gensim.models.word2vec import Word2Vec, LineSentence
from nltk.tokenize import sent_tokenize, word_tokenize

corpus_file = "../RelevantQuestionRetrival/MainCorpus.txt"


class Word2VecModel:
    def __init__(self):
        self.sentences = self.loadSentences()
        self.cores = multiprocessing.cpu_count()

    def loadSentences(self):
        with open(corpus_file,"r") as corpus:
            c = corpus.read()
            f = c.replace("\n", " ")
            data = []
            for i in sent_tokenize(f):
                temp = []
                for j in word_tokenize(i):
                    temp.append(j)
                data.append(temp)
            
            corpus.close()
        return data


    def create_model(self):
        num_features = 1000
        min_word_count = 1
        num_worker_threads = 40
        context_window = 10

        model = Word2Vec(self.sentences, workers=num_worker_threads, size=num_features, min_count=min_word_count,
                         window=context_window)

        model.save("MainWord2vec.model")
        print(model)
        return model

if __name__ == "__main__":
    test = Word2VecModel()
    test.create_model()
# The parameters:
# min_count = int - Ignores all words with total absolute frequency lower than this - (2, 100)
# window = int - The maximum distance between the current and predicted word within a sentence. E.g. window words on the left and window words on the left of our target - (2, 10)
# size = int - Dimensionality of the feature vectors. - (50, 300)
# sample = float - The threshold for configuring which higher-frequency words are randomly downsampled. Highly influencial. - (0, 1e-5)
# alpha = float - The initial learning rate - (0.01, 0.05)
# min_alpha = float - Learning rate will linearly drop to min_alpha as training progresses. To set it: alpha - (min_alpha * epochs) ~ 0.00
# negative = int - If > 0, negative sampling will be used, the int for negative specifies how many "noise words" should be drown. If set to 0, no negative sampling is used. - (5, 20)
# workers = int - Use these many worker threads to train the model (=faster training with multicore machines)
