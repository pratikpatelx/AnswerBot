import sys
import math
sys.path.append("../")
from UsefulAnswerParagraphsSelection.build_entropy_set import EntropyHandler
from UsefulAnswerParagraphsSelection.entity_overlap import EntityOverLap
from UsefulAnswerParagraphsSelection.patterns import PatternHandler
from UsefulAnswerParagraphsSelection.position import PositionHandler
from RelevantQuestionRetrival.RCA import RCA
import sqlite3

class answer(object):
    def __init__(self, an):
        self.ans = an
        self.relevance_score = 0
        self.entity_score = 0
        self.entropy_score = 0
        self.semantic_pattern = 0
        self.format_pattern = 0
        self.para_pos_score = 0
        self.overall_score = 0

class Normalize(object):

    def __init__(self):
        self.top_10 = []
        self.entropy = EntropyHandler()
        # entity = EntityOverLap()
        # pattern = PatternHandler()
        # position = PositionHandler()

    def calculate_entropy_val(self):
        
        entropy_max = 0
        entropy_min = 0

        scores = []
        for i in range(len(self.top_10)):
            idf_dict = self.entropy.calculate_IDF(self.top_10[i].ans)
            scores.append(self.entropy.calculate_entropy(idf_dict, self.top_10[i].ans))

        
        entropy_min = min(scores)
        entropy_max = max(scores)
        entropy_avg = sum(scores)/len(scores)
        selected_ans = []
        for i in range(len(scores)):
            if scores[i] >= entropy_avg:
                selected_ans.append([self.top_10[i], scores[i]])
                        # print(selected_ans)
                if entropy_max - entropy_min != 0:
                    self.top_10[i].entropy_score = ( scores[i]-entropy_min) / (entropy_max - entropy_min)
                else:
                    self.top_10[i].entropy_score = self.entropy_score - entropy_min
                

            print(self.top_10[i].entropy_score)

                # print(selected_ans)
                # if entropy_max - entropy_min != 0:
                #     self.entropy_score = (self.entropy_score -
                #                           entropy_min) / (entropy_max - entropy_min)
                # else:
                #     self.entropy_score = self.entropy_score - entropy_min

        return 0

    def main(self, top10Q):
        for i in range(len(top10Q)):
            self.top_10.append(answer(top10Q[i].ans))

        # a1 = answer("<p>Am I correct in saying that a .Net Hashtable is not synchronized while a Java Hashtable is? And at the same time a Java HashMap is not synchronized and has better performance? </p>\n\n<p>I am rewriting a Java app that makes heavy use of HashMaps in C# and I would like to use a HashTable and ensure that the performance is basically equivalent. </p>\n")
        # a2 = answer("<p>What are the differences between a <a href=https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/util/HashMap.html rel=noreferrer><code>HashMap</code></a> and a <a href=https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/util/Hashtable.html rel=noreferrer><code>Hashtable</code></a> in Java?</p>\n\n<p>Which is more efficient for non-threaded applications?</p>\n")
        
        # self.top_10 = [a1,a2]
        self.entropy_score = self.calculate_entropy_val()
        print(self.entropy_score)


if __name__ == "__main__":

    a1 = answer("<p>In your example this would assign the value <code>1</code> to <code>c</code> each time.</p><p><code>cr.next()</code> is effectively equivalent to <code>cr.send(None)</code></p>")
    a2 = answer("<p>The <code>yield</code> statement used in a function turns that function into a generator (a function that creates an iterator). The resulting iterator is normally resumed by calling <code>next()</code>. However it is possible to send values to the function by calling the method <code>send()</code> instead of <code>next()</code> to resume it:</p>")
    a3 = answer("<p>What are the differences between a <a href=https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/util/HashMap.html rel=noreferrer><code>HashMap</code></a> and a <a href=https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/util/Hashtable.html rel=noreferrer><code>Hashtable</code></a> in Java?</p>\n\n<p>Which is more efficient for non-threaded applications?</p>\n")
    ans = [a1,a2,a3]
    testing = Normalize()
    testing.main(ans)
