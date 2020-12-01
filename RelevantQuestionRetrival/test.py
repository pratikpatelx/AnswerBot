import sys
sys.path.append("../")
import IDFVocabulary.build_idf_voc as se
from gensim.models import Word2Vec
class Test:
    def __init__(self):
        return None

    def get_idf_metrics(self):
        """
        get_idf_metrics - This function gets the IDF metrics vocabulary
        that was created in IDFVocabulary.

        @return: the IDF vocabulary of metrics
        """
        test = se.IDFModel()
        idf_metric_dict = test.build_vocabulary()
        print(idf_metric_dict)
        return idf_metric_dict
    
    def get_word2_vec_model(self):
        """
        get_word2_vec_model - This function gets the Word 2 Vector model
        that was created in Word2VecModel directory
        @return: the Model 
        """
        model = Word2Vec.load("../Word2VecModel/word2vec.model")
        print(model)
        return model

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
        idf_metric_dict = self.get_idf_metrics()
        # the model we got from word2vec 
        model = self.get_word2_vec_model()
        for query in query_list:
            for question in Question_List:
                #calculate the similarity of the two word embeddings w[q] and w[Q]
                try:
                    rel = model.similarity(query, question)
                except:
                    rel = 0
                ## Add all the rel(W[q], W[Q]) into a list 
                total_rel = total_rel.append(rel)
            try:
                idf = idf_metric_dict[query]
            except:
                idf = 0

            max_rel = max(total_rel)
            rel_idf_summation.append(max_rel * idf)
            idf_values.append(idf)
        
        idf_summation = sum(idf_values)

        if idf_summation is not None:
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
    x.get_word2_vec_model()




# def funcname(parameter_list):
#     """
#     docstring
#     """
#     # TODO: COMPUTE REL
#     # rel(w[q], W[Q]) is the cosine similarity of the two word embeddings w[q] and w[Q]
#     # We can use word2VecModel to get the model and give it mode.similarity(w[q] and w[Q])
#     # then do a max of w[Q] and w[q]

#     # TODO: COMPUTE THE IDF METRIC
#     # idf(w[q], W[q])
#     pass
