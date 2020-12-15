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

    def tokenize_data(self, test_arr):
        stop_words = set(stopwords.words('english'))  
        ps = PorterStemmer()
        total_num = len(test_arr)
        voc = {}
        count = 0  
        for test in test_arr:
            clean = re.compile(r'<[^>]+>')
            result = re.sub(clean, '', test).strip("\n")
            tokens = word_tokenize(result)
            cur_word_set = set()
            words = [word for word in tokens if word.isalpha()]
            for w in words:
                w = w.lower()
                w = ps.stem(w)
                if w not in cur_word_set:
                    cur_word_set.add(w)
                    if w not in voc.keys():
                        voc[w] = 1.0
                    else:
                        voc[w] = voc[w] + 1.0
            count += 1
            if count == 1000:
                print('processing %s unit...' % count)
                break
        for key in voc.keys():
            idf = math.log(total_num / (voc[key] + 1.0))
            voc[key] = idf
            sorted_voc = sorted(voc.items())
        output = open("entropy_idf.txt", 'w', encoding="utf-8")
        data = str(sorted_voc)
        output.write(data)
        return sorted_voc


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
    temp = test.get_questions_data()
    x = test.tokenize_data(temp)
    # reponum = 50000
    # voc_str = ''
    # voc = test.read_entropy_voc()
    # for key in voc.keys():
    #     voc_str += (key + '   ' + str(voc[key]) + '\n')
    # test.write_to_file(path, voc_str.strip())
    # print('Done.')