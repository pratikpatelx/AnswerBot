import sqlite3
from sqlite3 import Error
from tokenize_text import Preprocess

class Question(object):
    """
    Data structure to store the Questions From the DB
    """
    def  __init__(self, id, title, body, tag):
        self.id = id
        self.title = title
        self.body = body
        self.tag = tag

    def __str__(self):
        """
        toString method to show contents of our objects
        """
        return("%10.4f  %s  %s  %s" % (self.id, self.title, self.body, self.tag))


class Corpus(Question):
    def __init__(self):
        self.dataList = []
        self.data_object = None

    def get_data(self):
        sql_query = "SELECT Id, Body, Title, Score, Tags FROM Posts WHERE SCORE>0;"
        try:
            connection = sqlite3.connect("../TestDB.db")
            cur = connection.cursor()
            cur.execute(sql_query)
            records = cur.fetchall()
            print("Total Rows are: ", len(records))
            count = 0
            for row in records:
                count = count +1
                # store the tile, body and tag in our data structure
                data_object = Question(row[0], row[2],row[1], row[4])
                data_object = Preprocess.preprocess_question(data_object)
                # print("Body: \n", row[0])
                # print("Title: \n", row[1])
                # print("Score: \n", row[2])
                # print("Tags: \n", row[3])
            cur.close()
        except sqlite3.Error as error:
            print("Failed to retrieve data from table..\n", error)
        finally:
            if connection:
                connection.close()
                print("The Sqlite Connection is now closed..\n")

    
if __name__ == "__main__":
    test = Corpus()
    test.get_data()
