import sys
sys.path.append("../")
import RelevantQuestionRetrival.RCA as rel
from nltk.tokenize import word_tokenize

class MMRHandler(object):

    def split_into_paragraphs(self, data):
            data = data.split("<p>")
            para = []
            for i in range(len(data)):
                if data[i] != '':
                    temp = data[i].split("</p>")
                    for j in range(len(temp)):
                        if temp[j].strip() != '':
                            para.append(temp[j]) 
            return para
        # for i in range(0, len(answers), 1):
    #         for j in range(0, i+1, 1):
    #             rel = relAlgo.calc_symmetric_relevance(ans_par[i], ans_par[j])
    #             matrix[i][j] = rel
    #             matrix[i][j] = rel

    def build_sim_matrix(self,ans_par, relAlgo):

        answers = []
        for i in range(len(ans_par)):
            answers.append(ans_par[i].ans)

        matrix = [[0 for col in range(len(answers))] for row in range(len(answers))]
        #print(matrix)
        print("doing matrix")
        for i in range(0, len(answers), 1):
            for j in range(0, i+1, 1):
                if i == j:
                    matrix[i][j] = 0.0
                else:
                    rel = relAlgo.calc_symmetric_relevance(answers[i], answers[j])
                    matrix[i][j] = rel
                    matrix[j][i] = rel

        # for i in range(0, len(answers), 1):
        #     for j in range(0, i, 1):
        #         # if i == j:
        #             matrix[i][j] = 1
        #         else:
        #             rel = relAlgo.calc_symmetric_relevance(answers[i], answers[j])
        #             matrix[i][j] = rel
        #             matrix[j][i] = rel

                """   1 2 3 4 5
                    1[1,y,z,a,b]
                    2[y,1, , , ]
                    3[z, ,1, , ]
                    4[a, , ,1, ]
                    5[b, , , ,1]
                """
        # tempstr = ""
        # for i in range(len(answers)):
        #     tempstr = tempstr + "["
        #     for j in range(len(answers)):
        #         tempstr = tempstr + str(matrix[i][j]) + ", "
        #     tempstr = tempstr + "]\n"

        #print(matrix)
        print("done matrix")
        reset = self.calculate_MMR(matrix)
        print(reset)
        for i in range(len(reset)):
            print("A:{} -> {}".format(i, answers[reset[i]]))
            print("\n--------------------------------------------------------------------------------------------------------\n")
            print("\n---------------------------------------------------------------------------------------------------------\n")


    # def build_sim_matrix(self, ans_par, relAlgo):

    #     answers = []
    #     for i in range(len(ans_par)):
    #         answers.append(ans_par[i].ans)

    #     matrix = [[0 for col in range(len(answers))] for row in range(len(answers))]
    #     #print(matrix)
    #     print("doing matrix")
    #     for i in range(0, len(answers), 1):
    #         for j in range(0, i+1, 1):
    #             if i == j:
    #                 matrix[i][j] = 0.0
    #             else:
    #                 rel = relAlgo.calc_symmetric_relevance(answers[i], answers[j])
    #                 matrix[i][j] = rel
    #                 matrix[j][i] = rel

    #     # for i in range(0, len(answers), 1):
    #     #     for j in range(0, i, 1):
    #     #         # if i == j:
    #     #             matrix[i][j] = 1
    #     #         else:
    #     #             rel = relAlgo.calc_symmetric_relevance(answers[i], answers[j])
    #     #             matrix[i][j] = rel
    #     #             matrix[j][i] = rel

    #             """   1 2 3 4 5
    #                 1[1,y,z,a,b]
    #                 2[y,1, , , ]
    #                 3[z, ,1, , ]
    #                 4[a, , ,1, ]
    #                 5[b, , , ,1]
    #             """
    #     # tempstr = ""
    #     # for i in range(len(answers)):
    #     #     tempstr = tempstr + "["
    #     #     for j in range(len(answers)):
    #     #         tempstr = tempstr + str(matrix[i][j]) + ", "
    #     #     tempstr = tempstr + "]\n"

    #     #print(matrix)
    #     print("done matrix")
    #     reset = self.calculate_MMR(matrix)
    #     print(reset)
    #     # for i in range(len(reset)):
    #     #     print("A:{} -> {}".format(i, answers[reset[i]]))
    #     #     print("\n--------------------------------------------------------------------------------------------------------\n")
    #     #     print("\n--------------------------------------------------------------------------------------------------------\n")
        



    def calculate_MMR(self, the_matrix):
        topnum = len(the_matrix)
        iteration = 1
        query_index = len(the_matrix)-1
        print("Query IDX:{0}".format(query_index))
        # init
        Set = []
        Rest = [i for i in range(len(the_matrix))]
        # parameter
        Lambda = 0.5
        while iteration <= topnum:
            # find most sim with query
            
            most_sim_with_query_index = -1
            max_dq_sim = -1
            for i in range(0, query_index, 1):
                if the_matrix[i][query_index] > max_dq_sim:
                    max_dq_sim = the_matrix[i][query_index]
                    most_sim_with_query_index = i
       
            if len(Set) == 0:
                # print("The SIM{0}".format(most_sim_with_query_index))
                Set.append(most_sim_with_query_index)
                Rest.remove(most_sim_with_query_index)
            else:
                max_MMR = -sys.float_info.max
                max_MMR_idx = -1
                for cur in Rest:
                    max_dd_sim = -sys.float_info.max
                    max_dd_idx = -1
                    for i in Set:
                        if the_matrix[cur][i] > max_dd_sim:
                            max_dd_sim = the_matrix[cur][i]
                            max_dd_idx = i
                    MRR_tmp = Lambda * the_matrix[cur][query_index] - (1 - Lambda) * the_matrix[cur][max_dd_idx]
                    if MRR_tmp > max_MMR:
                        print(MRR_tmp)
                        max_MMR = MRR_tmp
                        max_MMR_idx = cur
                
                # print("MMR {}".format(max_MMR_idx))
                if max_MMR_idx != -1:
                    Set.append(max_MMR_idx)
                    Rest.remove(max_MMR_idx)
            iteration += 1
            query_index = query_index - 1
        return Set
            


if __name__ == "__main__":
    test = MMRHandler()
    # ans_list = ["namedtuple is a factory function for making a tuple class","With that class we can create tuples that are callable by name also."]
    # x = test.build_sim_matrix(ans_list)
    sim_matrix = [[0, 0.9573873882875783, 0.9516797813496187, 0.9467918304642147, 0.9332049626816044, 0.9519011912389541, 0.9550946242694867, 0.9488732309749263], 
                    [0.9573873882875783, 0, 0.9644683221878154, 0.9598268104886541, 0.9470445106604071, 0.9608443920708933, 0.9682024894213855, 0.9619915417141993],
                    [0.9516797813496187, 0.9644683221878154, 0, 0.9660927293617942, 0.955062491972389, 0.9610783066267535, 0.9757787382967372, 0.9693677791397867], 
                    [0.9467918304642147, 0.9598268104886541, 0.9660927293617942, 0, 0.9515742243674324, 0.9608321951221315, 0.9691404384015092, 0.9667569433717564], 
                    [0.9332049626816044, 0.9470445106604071, 0.955062491972389, 0.9515742243674324, 0, 0.9447255128520036, 0.9599829754476228, 0.9543637344165523], 
                    [0.9519011912389541, 0.9608443920708933, 0.9610783066267535, 0.9608321951221315, 0.9447255128520036, 0, 0.9643653056565047, 0.9592323797830677], 
                    [0.9550946242694867, 0.9682024894213855, 0.9757787382967372, 0.9691404384015092, 0.9599829754476228, 0.9643653056565047, 0, 0.9726391789096014], 
                    [0.9488732309749263, 0.9619915417141993, 0.9693677791397867, 0.9667569433717564, 0.9543637344165523, 0.9592323797830677, 0.9726391789096014, 0]
                ]
    # sim_matrix = [ [0.9573873882875783, 0, 0.9644683221878154, 0.9598268104886541, 0.9470445106604071, 0.9608443920708933, 0.9682024894213855, 0.9619915417141993], 
    #                 [0.9516797813496187, 0.9644683221878154, 0, 0.9660927293617942, 0.955062491972389, 0.9610783066267535, 0.9757787382967372, 0.9693677791397867],
    #                 [0.9467918304642147, 0.9598268104886541, 0.9660927293617942, 0, 0.9515742243674324, 0.9608321951221315, 0.9691404384015092, 0.9667569433717564],
    #                 [0.9332049626816044, 0.9470445106604071, 0.955062491972389, 0.9515742243674324, 0, 0.9447255128520036, 0.9599829754476228, 0.9543637344165523],
    #                 [0.9519011912389541, 0.9608443920708933, 0.9610783066267535, 0.9608321951221315, 0.9447255128520036, 0, 0.9643653056565047, 0.9592323797830677],
    #                 [0.9550946242694867, 0.9682024894213855, 0.9757787382967372, 0.9691404384015092, 0.9599829754476228, 0.9643653056565047, 0, 0.9726391789096014],
    #                 [0.9488732309749263, 0.9619915417141993, 0.9693677791397867, 0.9667569433717564, 0.9543637344165523, 0.9592323797830677, 0.9726391789096014, 0]
    #             ]
    Set = test.calculate_MMR(sim_matrix)
    #print(Set)



# working code below

    # def split_into_paragraphs(self, data):
    #     data = data.split("<p>")
    #     para = []
    #     for i in range(len(data)):
    #         if data[i] != '':
    #             temp = data[i].split("</p>")
    #             for j in range(len(temp)):
    #                 if temp[j].strip() != '':
    #                     para.append(temp[j]) 
    #     return para
    # # for i in range(0, len(answers), 1):
    # #         for j in range(0, i+1, 1):
    # #             rel = relAlgo.calc_symmetric_relevance(ans_par[i], ans_par[j])
    # #             matrix[i][j] = rel
    # #             matrix[i][j] = rel


    # def build_sim_matrix(self, ans_par, relAlgo, query):
        
        
    #     answers = []
    #     for i in range(len(ans_par)):
    #         answers.append(ans_par[i].ans)


        

    #     #print(matrix)
    #     print("done matrix")
    #     reset = self.calculate_MMR(query, answers, relAlgo)
    #     print(reset)
    #     for i in range(len(reset)):
    #         print("A:{} -> {}".format(i, answers[reset[i]]))
    #         print("\n--------------------------------------------------------------------------------------------------------\n")
    #         print("\n--------------------------------------------------------------------------------------------------------\n")
        



    # def calculate_MMR(self, query, phrases, relAlgo):
    #     lambda_constant = 0
    #     threshold_terms = len(phrases)
    #     s = []
    #     r = phrases
    #     while len(r) > 0:
    #         score = 0
    #         phrase_to_add = ''
    #         for i in range(len(r)):
    #             first_part = relAlgo.calc_symmetric_relevance(query, r[i])
    #             second_part = 0
    #             for j in range(len(s)):
    #                 cos_sim = relAlgo.calc_symmetric_relevance(r[i], s[j][0])
    #                 if cos_sim > second_part:
    #                     second_part = cos_sim
    #             equation_score = lambda_constant*(first_part)-(1-lambda_constant) * second_part
    #             if equation_score > score:
    #                 score = equation_score
    #                 phrase_to_add = i
    #         if phrase_to_add == '':
    #             phrase_to_add = i
    #         print(phrase_to_add)
            
    #         s.append((r[phrase_to_add], score))
    #         r.remove(r[phrase_to_add])
    #     return (s, s[:threshold_terms])[threshold_terms > len(s)]







# down here

#






