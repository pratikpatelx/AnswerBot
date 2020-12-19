import sys
sys.path.append("../")
import RelevantQuestionRetrival.RCA as rel
from nltk.tokenize import word_tokenize

class MMRHandler(object):
    
    def build_sim_matrix(self, ans_par):
        relAlgo = rel.RCA()
        paragraph_len = len(ans_par)
        matrix = [[0 for col in range(paragraph_len)] for row in range(paragraph_len)]
        #print(matrix)

        for i in range(paragraph_len):
            ans_par[i] = word_tokenize(ans_par[i])

        for i in range(0, paragraph_len, 1):
            for j in range(0, i+1, 1):
                matrix[i][j] = relAlgo.calc_symmetric_relevance(ans_par[i], ans_par[j])
        print(matrix)
        return matrix
                


    def calculate_MMR(self, the_matrix):
        # topnum = 3
        # iteration = 1
        # query_index = len(the_matrix) - 1
        # # init
        # Set = []
        # Rest = [i for i in range(0, query_index - 1, 1)]
        # # parameter
        # Lambda = 0.5
        # while iteration <= topnum:
        #     # find most sim with query
        #     most_sim_with_query_index = -1
        #     max_dq_sim = -1
        #     for i in range(0, query_index, 1):
        #         if the_matrix[i][query_index] > max_dq_sim:
        #             max_dq_sim = the_matrix[i][query_index]
        #             most_sim_with_query_index = i
        #     if len(Set) == 0:
        #         Set.append(most_sim_with_query_index)
        #         Rest.remove(most_sim_with_query_index)
        #     else:
        #         max_MMR = -sys.float_info.max
        #         max_MMR_idx = -1
        #         for cur in Rest:
        #             max_dd_sim = -sys.float_info.max
        #             max_dd_idx = -1
        #             for i in Set:
        #                 if the_matrix[cur][i] > max_dd_sim:
        #                     max_dd_sim = the_matrix[cur][i]
        #                     max_dd_idx = i
        #             MRR_tmp = Lambda * the_matrix[cur][query_index] - (1 - Lambda) * the_matrix[cur][max_dd_idx]
        #             if MRR_tmp > max_MMR:
        #                 max_MMR = MRR_tmp
        #                 max_MMR_idx = cur
        #         Set.append(max_MMR_idx)
        #         Rest.remove(max_MMR_idx)
        #     iteration += 1
        # return Set


if __name__ == "__main__":
    test = MMRHandler()
    ans_list = ["namedtuple is a factory function for making a tuple class","With that class we can create tuples that are callable by name also."]
    x = test.build_sim_matrix(ans_list)
    sim_matrix = [[1, 0.11, 0.23, 0.76, 0.25, 0.91], [0.11, 1, 0.29, 0.57, 0.51, 0.90],
                  [0.23, 0.29, 1, 0.02, 0.20, 0.50], [0.76, 0.57, 0.02, 1, 0.33, 0.06],
                  [0.25, 0.51, 0.20, 0.33, 1, 0.63], [0.91, 0.90, 0.50, 0.06, 0.63, 1]]
    Set = test.calculate_MMR(sim_matrix)
    print(Set)
