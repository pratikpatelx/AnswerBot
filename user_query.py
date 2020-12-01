# program to request user query
import sqlite3
import time

#polishing is required: remind me if you see comment

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)


# At the moment looks like the best approach is LikeMethod but not sure yet
class LikeMethod:
    def __init__(self, db_name, questions, testMode):
        """
        docstring
        """
        self.test_Q = questions
        self.db_conn = create_connection(db_name)
        self.testMode = testMode

    def request_question(self):
        query = raw_input("\nQuestion: ")
        return query

    def request_test_question(self, test_question):
        temp_cursor = self.db_conn.cursor()
        post_ids = []
        tokens = test_question.split(' ')
        db_query = ("SELECT Id FROM posts where ")
        # Title like '%{}%'".format(tokens[i]))
        for i in range(len(tokens) - 1):
            db_query = db_query + ("Title like '%{}%' and ".format(tokens[i]))

        db_query = db_query + ("Title like '%{}%'".format(tokens[len(tokens)-1]))
                
        #print(db_query)

        temp_cursor.execute(db_query)
        result = temp_cursor.fetchall()
        
        for x in result:
            if x not in post_ids:
                post_ids.append(x[0])

        
    # if TRUE section 1 below will execute
    # if FALSE section 2 below will execute 
        up = False
    #change for testing speeds


#------------------------SECTION 1----------------------------------------------------------------------------------
# still deciding whether to keep or not for step 2 if main step doesnt produce much results. like google does it shows similar results
# if query doesnt have an exact match
# Too much noise from this method. for example it will show all the posts with the word "array" in the title for all words in a query
        #can be modified
        if len(result) < 5 and up:
            tokens = test_question.split(' ') #this is where you are tokenizing?
            for i in range(len(tokens)):
                if tokens[i] not in stopWords:
                    db_query = ("SELECT Id FROM posts where Title like '%{}%'".format(tokens[i]))
                    temp_cursor.execute(db_query)
                    result = temp_cursor.fetchall()

                    for x in result:
                        if x not in post_ids:
                            post_ids.append(x[0])
                else:
                    print("Stop Words removed: ", tokens[i])

        
        # else:
        #     print("Stop Words removed: ", tokens[i])
#-----------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------
#maybe this method could be step 2 if original method brings no results

        if len(result) < 5 and (not up):
            tokens = test_question.split(' ')
            db_query = ("SELECT Id FROM posts where ")
             # Title like '%{}%'".format(tokens[i]))
            for i in range(len(tokens) - 1):
                if tokens[i] not in stopWords:
                    db_query = db_query + ("Title like '%{}%' and ".format(tokens[i]))
                else:
                    print("Stop Word removed: ", tokens[i])


            if tokens[len(tokens)-1] not in stopWords:
                db_query = db_query + ("Title like '%{}%'".format(tokens[len(tokens)-1]))
            else:
                print("Ending Stop Word removed: ", tokens[i])

            print(db_query)    
            temp_cursor.execute(db_query)
            result = temp_cursor.fetchall()

            for x in result:
                if x not in post_ids:
                    post_ids.append(x[0])

#-------------------------------------------------------------------------------------------------------------------------
# main section continues here        
        print("-----------------------\ncount of Similar Q's from the database \n")
        count = 0
        for i in range(len(post_ids)):
            retrieve_query = ("SELECT Title FROM posts where id = {}".format(post_ids[i]))
            temp_cursor.execute(retrieve_query)
            result = temp_cursor.fetchall()
            
            if count < 10:
                print("Q{}: {}\n".format(post_ids[i],result[0][0].encode('utf-8')))
                count = count +1

        print("---------end---------")    
        print("Similar Question Count : {}".format(len(post_ids)))

    def test_function(self, db_conn):
        test_query = ("SELECT Id FROM posts where Title = NULL")
        test_cus = db_conn.cursor()
        test_cus.execute(test_query)
        test_result = test_cus.fetchall()
        print(len(test_result))


    def main(self):
        # self.test_function(db_conn)       
        print("Hello! I am AnswerBot. Ask me a technical question! Press <Enter> without a question to exit")
        count = 0
        while True:
            if self.testMode:
                if count >= len(self.test_Q):
                    #print("TEST Mode complete Switching to USER mode")
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

            self.request_test_question(query)
            end_time = time.time() - st_time
            print("Took {} seconds for Query: \"{}\"".format(end_time, query))


def retrieveStopWords(filename):
        file = open(filename, "r")
        for line in file:
            stopWords.append(line.strip())

        print("Got the stop words")

stopWords = []
if __name__ == "__main__":
    retrieveStopWords("./Word2VecModel/stopWords.txt")
    testQuestions = []
    testMode = True
    ini = LikeMethod("pythonsqlite.db", testQuestions, testMode)
    ini.main()

            





















# class WordMethod:
    
#     def __init__(self):
#         """
#         docstring
#         """

#     def request_question(self):
#         query = raw_input("\nQuestion: ")
#         return query

#     def request_test_question(self,db_conn, test_question):
#         temp_cursor = db_conn.cursor()
#         post_ids = []
#         tokens = test_question.split(' ')
#         for i in range(len(tokens)):
#             if tokens[i] not in stopWords:
#                 db_query = ("SELECT Id FROM posts where Title like '%{}%'".format(tokens[i]))
#                 temp_cursor.execute(db_query)
#                 result = temp_cursor.fetchall()

#                 for x in result:
#                     if x not in post_ids:
#                         post_ids.append(x[0])
#             else:
#                 print("Stop Words removed: ", tokens[i])

#         print("-----------------------\ncount of Similar Q's from the database \n")
#         count = 0
#         for i in range(len(post_ids)):
#             retrieve_query = ("SELECT Title FROM posts where id = {}".format(post_ids[i]))
#             temp_cursor.execute(retrieve_query)
#             result = temp_cursor.fetchall()
#             if count < 10:
#                 # print(result.strip())
#                 print("Q{}: {}\n".format(post_ids[i],result[0][0].encode('utf-8')))
#                 count = count + 1

#         print("---------end---------")    
#         print(len(post_ids))

#     def test_function(self, db_conn):
#         test_query = ("SELECT Id FROM posts where Title = NULL")
#         test_cus = db_conn.cursor()
#         test_cus.execute(test_query)
#         test_result = test_cus.fetchall()
#         print(len(test_result))


#     def main(self):
#         db = "pythonsqlite.db"
#         db_conn = create_connection(db) 
#         # self.test_function(db_conn)       
#         print("Hello! I am AnswerBot. Ask me a technical question! Press <Enter> without a question to exit")
#         while True:
#             query = self.request_question()
#             st_time = time.time()
#             if query == '':
#                 print("Closing AnswerBot... \nSee you soon! \nGoodBye...")
#                 break

#             self.request_test_question(db_conn, query)
#             end_time = time.time() - st_time
#             print("Took {} seconds for Query {}".format(end_time, query))


    



