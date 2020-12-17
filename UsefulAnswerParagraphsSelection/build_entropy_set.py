import sqlite3
import sys
sys.path.append("../")
path = "entropy_idf.txt"
import re
import math
from nltk.corpus import stopwords  
from nltk.stem import PorterStemmer 
from nltk.tokenize import word_tokenize

class EntropyHandler(object):

    def get_questions_data(self):
        """
        get_questions_data: This method gets the data from the database
        @return: returns the list containg data from the DB
        """
        database = "../pythonsqlite.db"
        sql_statement = 'SELECT * FROM Posts;'
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        dataList = []
        try:
            cur.execute(sql_statement)
            rows = cur.fetchall()
            count = 0
            for row in rows:
                count = count + 1
                ans = row[7]
                dataList.append(ans)
        except Exception as e:
            print(e)
        finally:
            cur.close()
            conn.close()
        return dataList

    def calculate_IDF(self, test_arr):
        # stop_words = set(stopwords.words('english'))
        N = len(test_arr)  
        ps = PorterStemmer()
        word_freq = {}
        count = 0  
        for test in test_arr:
            test = test.lower()
            clean = re.compile(r'<[^>]+>')
            test = re.sub(r'\W',' ',test)
            test = re.sub(r'\s+',' ',test)
            result = re.sub(clean, '', test)
            tokens = word_tokenize(result)
            words = [word for word in tokens if word.isalpha()]
            for token in words:
                token = ps.stem(token)
                if token not in word_freq.keys():
                    word_freq[token] = 1
                else:
                    word_freq[token] += 1
            count += 1
            if count == 1000:
                print('processing %s unit...' % count)
                break
        for key, value in word_freq.items():
            word_freq[key] = math.log(N / float(value))
        print("{0:20} {1:20}".format("Word", "IDF VALUE"))
        for key, value in word_freq.items():
            print("{0:20} {1:20}".format(key, value))
        return word_freq

        


    def read_entropy_voc(self):
        the_file = open(path)
        idf_voc = {}
        for line in the_file:
            word_idf = line.split('     ')
            word = word_idf[0]
            idf = float(word_idf[1].strip())
            idf_voc[word] = idf
        return idf_voc

if __name__ == '__main__':
    test = EntropyHandler()
    temp = ["It is going to rain today", "Today I am not going outside.", "I am going to watch the season premiere."]
    x = test.calculate_IDF(temp)