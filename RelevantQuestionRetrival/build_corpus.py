import sqlite3

import sys
sys.path.append("../")
import utils.tokenize_text as pe

class Question(object):
    """
    Data structure to store the Questions From the DB
    """

    def __init__(self, id, title, body, tag):
        self.id = id
        self.title = title
        self.body = body
        self.tag = tag

    def __str__(self):
        """
        toString method to show contents of our objects
        """
        return "%10.4f  %s  %s  %s" % (self.id, self.title, self.body, self.tag)


class Corpus(Question):
    """
    Corpus - This class is used to build the text corpus from
    the DB
    """
    def __init__(self):
        """
        initialize an empty object
        """
        pass

    @staticmethod
    def get_data():
        """
        get_data() - This method will get the Data required to build the text corpus from the DB
        @return: a List containg the data from the DB
        """
        sql_query = "SELECT Id, Body, Title, Score, Tags FROM Posts WHERE SCORE>0 AND (Title is NOT NULL);"
        try:
            # initialize a connection to the DB
            connection = sqlite3.connect("../TestDB.db")
            cur = connection.cursor()
            dataList = []
            cur.execute(sql_query)
            records = cur.fetchall()
            print("Total Rows are: ", len(records))
            count = 0
            for row in records:
                count = count + 1
                # store the tile, body and tag in our data structure
                data_object = Question(row[0], row[2], row[1], row[4])
                data_object = pe.preprocess_question(data_object)
                dataList.append(data_object)
                # print(data_object.tag)
                # print("Body: \n", row[0])
                # print("Title: \n", row[1])
                # print("Score: \n", row[2])
                # print("Tags: \n", row[3])
                if len(dataList) % 10000 == 0:
                    print("The Load of Questions is {}....".format(len(dataList)))
            cur.close()
            return dataList
        except sqlite3.Error as error:
            print("Failed to retrieve data from table..\n", error)
        finally:
            if connection:
                connection.close()
                print("The Sqlite Connection is now closed..\n")

    def main(self):
        """
        Main method that adds our text from the list to
        a txt file creating the text corpus
        @todo: WORK ON REFACTORING THIS CODE
        @return:
        @rtype:
        """
        corpus_file = 'corpus.txt'
        data_list = self.get_data()
        print("Starting to Add Data to the txt file....")
        with open(corpus_file, 'w', encoding="utf-8") as filehandler:
            for d in data_list:
                filehandler.write(str(d.title) + " " + str(d.body) + "\n")
        print("Added Data Successfully to the txt file...\n")


if __name__ == "__main__":
    test = Corpus()
    test.main()
