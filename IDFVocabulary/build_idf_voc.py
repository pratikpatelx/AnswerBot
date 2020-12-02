import sqlite3
import sys
sys.path.append("../")
from nltk import word_tokenize

import RelevantQuestionRetrival.build_corpus as Q
import operator
import math as m
import csv

class DatabaseHandler:
    def __init__(self):
        """
        DatabaseHandler Class: used to manage SQLite connection and queries
        """
        self.dataList = []

    def create_connection(self, database):
        """
        create_connection: This method createas a connection the sqlite database
        @database: the database name
        @return: returns a connection to the database
        """
        conn = None
        try:
            conn = sqlite3.connect(database)
        except sqlite3.Error as e:
            print(e)
        return conn

    def get_questions_data(self):
        """
        get_questions_data: This method gets the data from the database
        @return: returns the list containg data from the DB
        """
        database = "../pythonsqlite.db"
        sql_statement = 'SELECT * FROM Posts WHERE Title is NOT NULL;'
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        try:
            cur.execute(sql_statement)
            rows = cur.fetchall()
            count = 0
            for row in rows:
                count = count + 1
                data_object = Q.Question(row[0], row[14], row[7], row[15])
                self.dataList.append(data_object)
        except Exception as e:
            print(e)
        finally:
            cur.close()
            conn.close()
        return self.dataList

class IDFModel:

    def __init__(self):
        """
        IDFModel : This class implementes the IDF metrics required to train the classifier
        """
        self.voc_dict = {}
        self.count = 0
        self.temp = DatabaseHandler()

    def build_vocabulary(self):
        """
        build_vocabulary: This methods builds a IDF vocabulary from the Data gathered
        @return: return's the dictonary of a sorted vocabulary of questions and titles
        """
        self.questions_list = self.temp.get_questions_data()
        total_count = len(self.questions_list)
        for question in self.questions_list:
            tokenized_title = word_tokenize(question.title.strip())
            current_word_set = set()
            for title in tokenized_title:
                if title not in current_word_set:
                    current_word_set.add(title)

                    if title not in self.voc_dict:
                        self.voc_dict[title] = 1.0
                    else:
                        self.voc_dict[title] = self.voc_dict[title] + 1.0 

            self.count = self.count + 1
            if self.count % 10000 == 0:
                print("The Processing has reached: {}\n".format(self.count))
        
        for key in self.voc_dict.keys():
            idf_val = m.log(total_count / (self.voc_dict[key] + 1.0))
            self.voc_dict[key] = idf_val
            
        getcount = operator.itemgetter(1)
        sorted_vocabulary = sorted(self.voc_dict.items(), key=getcount)
        return sorted_vocabulary
    
    def convert_list_to_csv(self, the_list, csv_path, header):
        """
        convert_list_to_csv: This method convertes the sorted IDF vocabulary
                              to a CSV file which can be used to analyze IDF metrics
        @the_list : the list of IDF vocabulary
        @csv_path : the path to where the CSV file will be created
        @header: The headings in the CSV file
        """
        with open(csv_path, 'w', encoding="utf-8") as filehandler:
            mycsv = csv.writer(filehandler)
            mycsv.writerow(header)
            for row in the_list:
                try:
                    mycsv.writerow(row)
                except Exception as e:
                    print("Error Failed to add data to the csv...\n", e)
        print("Successfully Wrote Data to the csv at %s..\n " % csv_path)

    def main(self):
        """
        main : This method creates the IDF CSV and Vocabulary
        """
        csv_file = "IDF_Test.csv"
        header = ['Word', 'IDF']
        vocabulary = self.build_vocabulary()
        self.convert_list_to_csv(vocabulary, csv_file, header)

if __name__ == "__main__":
    testIDF = IDFModel()
    testIDF.main()