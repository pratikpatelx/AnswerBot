import sys
sys.path.append("../")

import sqlite3

from UsefulAnswerParagraphsSelection.entity_overlap import EntityOverLap



class Normalize(object):

    def __init__(self):
        self.relevance_score = 0
        self.entity_score = 0
        self.entropy_score = 0
        self.semantic_pattern = 0
        self.format_pattern = 0
        self.para_pos_score = 0
        self.overall_score = 0
        

    def read_answers_from_table(self, test_str):
        corr_answers = {}
        conn = sqlite3.connect('../pythonsqlite.db')
        curr = conn.cursor()
        try:
            for (q_id, sim) in test_str:
                corr_answer = []
                query = "SELECT * FROM Posts WHERE Body IS NOT NULL AND PostTypeId = 2 AND ParentID = " +str(q_id)
                #print(query)
                curr.execute(query)
                results = curr.fetchall()
                for row in results:
                    # corr_answer.append(row[0])
                    corr_answer.append(row[7])
                    #corr_answer.append(row[4])
                    #corr_answer.append(row[17])
                    #print(corr_answer)
                corr_answers[q_id] = corr_answer
        except Exception as e:
            print("Error".format(e))
        
        curr.close()
        conn.close()
        # print(corr_answers.items())
        return corr_answers

    def split_into_paragraph(self,text):
        # extract <p>sent</p>
        paragraph_list = []
        tag_head = '<p>'
        tag_tail = '</p>'
        while tag_head in text:
            head_pos = text.find(tag_head)
            tail_pos = text.find(tag_tail)
            if head_pos >= tail_pos:
                break
            ahref_head = text[head_pos:tail_pos].find(">")
            tag_content = text[head_pos + ahref_head + 1:tail_pos]
            text = text[:head_pos] + text[tail_pos + len(tag_tail):]
            if tag_content != '':
                paragraph_list.append(tag_content)
        return paragraph_list

    def remove_text_code(self, html_str):
        import re
        # regex: <pre(.*)><code>([\s\S]*?)</code></pre>
        regex_pattern = r'<pre(.*?)><code>([\s\S]*?)</code></pre>'
        html_text = html_str
        for m in re.finditer(regex_pattern, html_str):
            raw_code = html_str[m.start():m.end()]
            # remove code
            html_text = html_text.replace(raw_code, " ")
        return html_text.replace('\n', ' ')
    
    def clean_html_tags2(self, raw_html):
        import re
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext
    
    def remove_html_tags(self, raw_html):
        from bs4 import BeautifulSoup
        try:
            text = BeautifulSoup(raw_html, "html.parser").text
        except Exception as e:
            # UnboundLocalError
            text = clean_html_tags2(raw_html)
        finally:
            return text.encode('utf8')
        
    def preprocessing_for_ans_sent(self, sent):
        text = self.remove_text_code(sent.lower())
        text = self.remove_html_tags(text)
        #text = self.replace_double_space(text.replace('\n', ' '))
        return text.strip()
    
    def replace_double_space(self,text):
        while '  ' in text:
            text = text.replace('  ', ' ')
        return text



    def set_up_entity(self, query_word,top_relevant_paragraph_num, top_dq_id_and_sim):
        ne = EntityOverLap()
        answers_list = self.read_answers_from_table(top_dq_id_and_sim)
        #print(answers_list)
        the_query_words = query_word
        query_entities = ne.get_entities(the_query_words)
        for (q_id, sim) in top_dq_id_and_sim:
            answers = answers_list[q_id]
            for answer_tmp in answers:
                answer_body = answer_tmp
                print(answer_body)
                sentences = self.split_into_paragraph(answer_body)
                order = 1

                for sent in sentences:
                    clean_sent = self.preprocessing_for_ans_sent(sent)
                    entity = ne.calc_entity(query_entities, clean_sent)
                    print(entity)




    
    # def start_normalization(self, relevance_min, relevance_max, entropy_min, entropy_max, min_vote, max_vote):
    
    def load_qs_result(self, rq_path):
        import pandas as pd
        rq_result = []
        df = pd.read_csv(rq_path)
        for idx, row in df.iterrows():
            rq_result.append([row[0], eval(row[1])])
        return rq_result


if __name__ == "__main__":
    temp = Normalize()
    print("Starting....")
    rq_res_fpath = "../rq_res.csv"
    res = []
    top_relevant_paragraph_num = 10
    for query, top_dq_id_and_sim in temp.load_qs_result(rq_res_fpath):
        print(top_dq_id_and_sim)
        # top_ss = temp.set_up_entity(query, top_relevant_paragraph_num, top_dq_id_and_sim)
        for i in range(10):
            print("#%s\nsent: %s\n\n" % (i, top_ss[i]))
        res.append([query, top_ss])
