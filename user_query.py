# # program to request user query
# user_query.py : This file gets the querys from the DB dynamically based on user input
# and displays the results
# Authors: Pratik Patel, Swetul Patel
# Created on: 12/2/2020
import sqlite3
import time
import RelevantQuestionRetrival.RCA as rel
import UsefulAnswerParagraphsSelection.normalization as Normalize
import DiverseAnswerSummaryGeneration.MMR as MMR
import nltk
import re

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Connecting to DB...")
        return conn
    except Exception as e:
        print(e)


class Q_data:
    def __init__(self, ques, rele, id):
        self.Q = ques
        self.Rel = rele
        self.Id = id
        self.ans = ""
        self.tags = ""
        self.ans_score = 0
        self.ansId = 0


class AnswerBot:
    def __init__(self, db_name, questions, testMode):
        """
        AnswerBot: This class mimics the AnswerBot implementation, creates a query on the 
                    Database and prints out the results 
        """
        self.test_Q = questions
        self.db_conn = create_connection(db_name)
        self.testMode = testMode

    def request_question(self):
        """
        request_question: This method is used to request a question query from the DB
        @return : returns the query
        """
        query = input("\nQuestion: ")
        return query

    def request_test_question(self, test_question):
        """
        request_test_question: This method fetches the Titles  and Questions from the Posts table
        based on the user query 
        @test_question: the question to be asked
        @return: returns the POST ID's relevant to the Title and Question 
        """
        temp_cursor = self.db_conn.cursor()
        post_ids = []
        tokens = test_question.split(' ')
        db_query = ("SELECT Id, Title FROM posts where ")

        for i in range(len(tokens) - 1):
            db_query = db_query + ("Title like '%{}%' and ".format(tokens[i]))

        db_query = db_query + ("Title like '%{}%'".format(tokens[len(tokens)-1]))

        temp_cursor.execute(db_query)
        result = temp_cursor.fetchall()
        #print(len(result))
        for x in result:
            if x not in post_ids:
                post_ids.append(x)

        if len(post_ids) <= 3:
            tags = []
            tokens = test_question.split(' ')
            db_query = ("SELECT DISTINCT Id, Title FROM Posts where ")
            for i in range(len(tokens)):
                if tokens[i] not in stopWords:
                    temp_query = 'SELECT Id FROM Tags where TagName like "%{}%";'.format(
                        str(tokens[i]))
                    temp_cursor.execute(temp_query)
                    result = temp_cursor.fetchall()
                    if len(result) > 0 and len(result) < 200:
                        if tokens[i] not in tags:
                            tags.append(tokens[i])
                
            for i in range(len(tags)):
                if i < len(tags)-1:
                    db_query = db_query + "Title like '%{}%' and ".format(tags[i])
                else:
                    db_query = db_query + "Title like '%{}%'".format(tags[len(tags)-1]) 

            temp_cursor.execute(db_query)
            result = temp_cursor.fetchall()
            #print(len(result))
            for x in result:
                if x not in post_ids:
                    post_ids.append(x)
            if(len(result) <= 3):
                db_query = ("SELECT DISTINCT Id, Title FROM Posts where ")
                for i in range(len(tags)):
                    if i < len(tags)-1:
                        db_query = db_query + "Title like '%{}%' or ".format(tags[i])
                    else:
                        db_query = db_query + "Title like '%{}%'".format(tags[len(tags)-1])
                
                temp_cursor.execute(db_query)
                result = temp_cursor.fetchall()
                #print(len(result))
                for x in result:
                    if x not in post_ids:
                        post_ids.append(x)
        print("---------end---------")
        print("Similar Question Count : {}".format(len(post_ids)))

        return post_ids

    def main(self):
        """
        main: This method will run the Query dynamically based on what the user types. 
        Then it will calculate the overall score to get the correct N number of answer
        paragraphs. The score is going to be normalized from normalization.py
        """
        print("\nHello! I am AnswerBot. Ask me a technical question! Press <Enter> without a question to exit")
        count = 0
        while True:
            if self.testMode:
                if count >= len(self.test_Q):
                    self.testMode = False
                    query = self.request_question()
                else:
                    query = self.test_Q[count]
                    count = count + 1
            else:
                query = self.request_question()

            st_time = time.time()
            if query == '':
                print("Closing AnswerBot... \nSee you soon! \nBye...")
                break

            # calculating the relevance of the each question
            questions = self.request_test_question(query)
            query_list = nltk.sent_tokenize(query)
            query_list = self.preprocess(query_list)
            tokens = nltk.word_tokenize(query_list[0])
            processed_Q = {}
            answers = []

            for Q in questions:
                Q_list = nltk.sent_tokenize(Q[1])
                Q_list = self.preprocess(Q_list)
                sentence_tokens = nltk.word_tokenize(Q_list[0])
                temp_rel = relAlgo.calc_symmetric_relevance(
                    tokens, sentence_tokens)
                processed_Q[Q[0]] = [Q[1], temp_rel]
                answers.append(Q_data(Q[1], temp_rel, Q[0]))
                #print("Relevance: [{}] Q: [{}]".format(temp_rel, Q[1]))


            # collect top 10 answers
            # answers.sort(key=lambda x: x.Rel, reverse=True)
            answers = sorted(answers, key=lambda x: x.Rel, reverse=True)
            top_10 = []
            ans_cursor = self.db_conn.cursor()
            for i in range(len(answers)):
                if i <= 10:
                    db_query = 'SELECT AcceptedAnswerId, tags FROM posts Where Id = {}'.format(
                        answers[i].Id)
                    ans_cursor.execute(db_query)
                    result = ans_cursor.fetchall()
                    answers[i].tags = result[0][1]
                    answers[i].ansId = result[0][0]
                    # print("--------===========--------------------==============----------")
                    if result[0][0] != None:
                        db_query = 'SELECT Body, Score FROM posts Where Id = {}'.format(
                            result[0][0])
                        ans_cursor.execute(db_query)
                        result = ans_cursor.fetchall()
                        answers[i].ans = result[0][0]
                        answers[i].ans_score = result[0][1]
                        
                        top_10.append(answers[i])
                    #print("Relevance: [{:.3f}] Q: {}".format(answers[i].Rel, answers[i].Q))
                    else:
                        #print("***********************---DELETE---**************************")
                        del answers[i]
                else:
                    break
            
            # create pool of paragraphs from all top 10 paragraphs
            answer_para = []
            for i in range(len(top_10)):
                result = self.split_into_paragraphs(top_10[i].ans)
                for j in range(len(result)):
                    a1 = Q_data(top_10[i].Q,top_10[i].Rel, top_10[i].Id)
                    a1.ans = result[j]
                    a1.tags = top_10[i].tags
                    a1.ans_score = top_10[i].ans_score
                    a1.ansId = top_10[i].ansId
                    answer_para.append(a1)

            
            print(len(answer_para))

            feature_scores = Normalize.Normalize()
            print("--------------------------------------------------------------------\n---------------------\n")
            sorted_ans = feature_scores.main(answer_para, relAlgo.idf_dict, stopWords)
            print(len(sorted_ans))
            MMRHandler = MMR.MMRHandler()
            MMRHandler.build_sim_matrix(sorted_ans, relAlgo)
            print("--------------------------------------------------------------------\n---------------------\n")
            # print(len(sorted_ans))
            # for i in range(len(sorted_ans)):
            #     print("A:{} SC:{} -> {}".format(i, sorted_ans[i].overall_score, sorted_ans[i].ans))
            #     # result = MMRHandler.build_sim_matrix(sorted_ans[i].ans, relAlgo)
            #     if i > 5:
            #         break  
            #     #print(result)

            end_time = time.time() - st_time
            print("\nTook {:.2f} seconds for Query: \"{}\"".format(
                    end_time, query))

        self.db_conn.close()

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
    
    def preprocess(self, item):
        """
        preprocess: This method preprocess the text i.e removed unwanted tags, spaces etc
                    using regular expression
        @item: the text to be preprocessed
        @return: returns the preprocessed text
        """
        for i in range(len(item)):
            item[i] = item[i].lower()
            item[i] = re.sub(r'\W', ' ', item[i])
            item[i] = re.sub(r'\s+', ' ', item[i])

        return item


def retrieveStopWords(filename):
    """
    retrieveStopWords: this method gets the stop words file "stopWords.txt" from the 
                        project directory
    """
    file = open(filename, "r")
    for line in file:
        stopWords.append(line.strip())


# FOR TESTING PURPOSES
stopWords = []
relAlgo = rel.RCA()
if __name__ == "__main__":
    retrieveStopWords("./Word2VecModel/stopWords.txt")
    testQuestions = ["Difference between hashtable and hashmap"]
    # testQuestions = ["Differe"]
    # "How do I compare strings in Java?", "Why is processing a sorted array faster than processing an unsorted array?"
    testMode = True
    begin = AnswerBot("pythonsqlite.db", testQuestions, testMode)
    begin.main()
