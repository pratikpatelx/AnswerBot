from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
import math
import re
import sqlite3
import sys
sys.path.append("../")
path = "entropy_idf.txt"


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

    def calculate_IDF(self, test):
        # stop_words = set(stopwords.words('english'))
        test = test.lower()
        clean = re.compile(r'<[^>]+>')
        test= re.sub(r'<p>', '', test)
        test= re.sub(r'</p>', '', test)
        test = re.sub(r'\W', ' ', test)
        test = re.sub(r'\s+', ' ', test)
        result = re.sub(clean, '', test)
        tokens = word_tokenize(test)
        N = len(tokens)
        ps = PorterStemmer()
        word_freq = {}
        count = 0
        words = [word for word in tokens if word.isalpha()]
        for token in words:
            token = ps.stem(token)
            if token not in word_freq.keys():
                word_freq[token] = 1
            else:
                word_freq[token] += 1

        for key, value in word_freq.items():
            word_freq[key] = math.log(N / float(value))
    
        return word_freq

    def calculate_entropy(self,stopWords, idf_dict, ans):
        
        # print("{0:20} {1:20}".format("Word", "IDF VALUE"))
        # for key, value in idf_dict.items():
        #     print("{0:20} {1:20}".format(key, value))

        test = ans.lower()
        clean = re.compile(r'<[^>]+>')
        test = re.sub(r'\W', ' ', test)
        test = re.sub(r'\s+', ' ', test)
        result = re.sub(clean, '', test)
        tokens = word_tokenize(test)
        N = len(tokens)
        ps = PorterStemmer()
        word_freq = {}
        count = 0
        words = [word for word in tokens if word.isalpha()]
        idf_list = []
        for token in words:
            # token = ps.stem(token)
            if token not in stopWords:
                try:
                    idf_val = float(idf_dict[token])
                except Exception as e:
                    #print(e)
                    idf_val = 0

                idf_list.append(idf_val)

        total_entropy = sum(idf_list)
        return total_entropy

    def read_entropy_voc(self):
        the_file = open(path)
        idf_voc = {}
        for line in the_file:
            word_idf = line.split(' ')
            word = word_idf[0]
            idf = float(word_idf[1].strip())
            idf_voc[word] = idf
        return idf_voc

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



if __name__ == '__main__':
    import re
    data = "<p>hashtable is fast compred to hashmap</p> <p>i coundnt agree more</p>"
