# # program to request user query
# user_query.py : This file gets the querys from the DB dynamically based on user input
# and displays the results 
# Authors: Pratik Patel, Swetul Patel
# Created on: 12/2/2020
import sqlite3
import time
import RelevantQuestionRetrival.RCA as rel 
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
    def __init__(self, ques, rele):
        self.Q = ques
        self.Rel = rele

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
        for x in result:
            if x not in post_ids:
                post_ids.append(x)

        if len(post_ids) <= 3:
            tokens = test_question.split(' ')
            db_query = ("SELECT Id, Title FROM Posts where ")
            for i in range(len(tokens) - 1):
                if tokens[i] not in stopWords:
                    db_query = db_query + ("Title like '%{}%' or ".format(tokens[i]))
                
            if tokens[len(tokens)-1] not in stopWords:
                db_query = db_query + ("Title like '%{}%'".format(tokens[len(tokens)-1]))
            
            temp_cursor.execute(db_query)
            result = temp_cursor.fetchall()
            print(len(result))
            for x in result:
                if x not in post_ids:
                    post_ids.append(x)
        print("---------end---------")    
        print("Similar Question Count : {}".format(len(post_ids)))

        return post_ids

    def main(self):
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
                temp_rel = relAlgo.calc_symmetric_relevance(tokens, sentence_tokens)
                processed_Q[Q[0]] = [Q[1], temp_rel]
                answers.append(Q_data(Q[1], temp_rel))
                print("Relevance: [{}] Q: [{}]".format(temp_rel,Q[1]))

            answers.sort(key=lambda x: x.Rel, reverse=True)
            for i in range(len(answers)):
                if i <= 10:
                    print("Relevance: [{:.3f}] Q: {}".format(answers[i].Rel,answers[i].Q))
                else:
                    break
            end_time = time.time() - st_time
            print("\nTook {:.2f} seconds for Query: \"{}\"".format(end_time, query))

        self.db_conn.close()


    def preprocess(self, item):
        """
        preprocess: This method preprocess the text i.e removed unwanted tags, spaces etc
                    using regular expression
        @item: the text to be preprocessed
        @return: returns the preprocessed text
        """
        for i in range(len(item)):
            item[i] = item[i].lower()
            item[i] = re.sub(r'\W',' ',item[i])
            item[i] = re.sub(r'\s+',' ',item[i])
        
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
    testQuestions = ["Differences between HashMap and Hashtable?"]
    testMode = True
    begin = AnswerBot("pythonsqlite.db", testQuestions, testMode)
    begin.main()