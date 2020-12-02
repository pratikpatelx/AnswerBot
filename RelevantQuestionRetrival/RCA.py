# RCA.py : This file gets the IDF metrics, Word2Vec Model and Calculates the Asymmetric and Symmetric 
# Relevance between a user query q and Question Q
# Authors: Pratik Patel, Swetul Patel
# Created on: 12/2/2020
import sys
sys.path.append("../")
import IDFVocabulary.build_idf_voc as se
from gensim.models import Word2Vec
from nltk.tokenize import sent_tokenize, word_tokenize
import csv
class RCA:
    def get_idf_metrics(self):
        """
        get_idf_metrics - This function gets the IDF metrics vocabulary
        that was created in IDFVocabulary.

        @return: the IDF vocabulary of metrics
        """
        idf_metric_dict = {}
        with open("IDFVocabulary/IDF_Test.csv") as csvfile:
            readCSV = csv.reader(csvfile, delimiter = ',')
            print("Loading IDF metrics....")
            for row in readCSV:
                idf_metric_dict[row[0]] = row[1]
        
        print("{} IDF metric words loaded.".format(len(idf_metric_dict)))
        return idf_metric_dict
    
    def get_word2_vec_model(self):
        """
        get_word2_vec_model - This function gets the Word 2 Vector model
        that was created in Word2VecModel directory
        @return: the Model 
        """
        print("Loading Word2Vector Model.\n Please wait....")
        model = Word2Vec.load("./Word2VecModel/MainWord2vec.model")
        print("Loaded model details : {}".format(model))
        return model


    def __init__(self):
        self.idf_dict = self.get_idf_metrics()
        self.word2Vec = self.get_word2_vec_model()

    def calc_asymmetric_val(self,query_list, Question_List):
        """
        calc_asymmetric_val - This function calculates the asymetric relevance
        between the query q and the title of a question Q.

        @return - the asymmetric value calculated
        """
        #list of total relevance of IDFs
        rel_idf_summation = []
        # list of total IDF metrics
        idf_values = []
        # A set of IDF metric dictionary's
        for query in query_list:

            total_rel = []
            for question in Question_List:
                #calculate the similarity of the two word embeddings w[q] and w[Q]
                try:
                    rel = self.word2Vec.similarity(query, question)
                except Exception as e:
                    rel = 0
                ## Add all the rel(W[q], W[Q]) into a list 
                total_rel.append(rel)
            try:
                idf_val = self.idf_dict[query]
                idf = float(idf_val)
                
            except:
                idf = 0

            max_rel = max(total_rel)
            rel_idf_summation.append(max_rel * idf)
            idf_values.append(idf)
        
        idf_summation = sum(idf_values)

        if idf_summation != 0:
            asymmetric_rel = sum(rel_idf_summation) / idf_summation
        else:
            asymmetric_rel = 0

        return asymmetric_rel

    def calc_symmetric_relevance(self, query_list, Question_List):
        """
        calc_symmetric_relevance - This method calculates the
        symmetric relevance from the asymmetric relevance to get a
        more weight towards the relevance measurement between the query
        and the question title.
        
        @return: return's the average symmetric relevance value
        """
        rel_q_to_Q = self.calc_asymmetric_val(query_list, Question_List)
        rel_Q_to_q = self.calc_asymmetric_val(Question_List, query_list)
        average_relevance = (rel_q_to_Q + rel_Q_to_q) / 2
        return average_relevance

# For testing purposes
if  __name__ == "__main__":
    x = Test()