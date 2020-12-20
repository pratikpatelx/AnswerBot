import sys
import math
sys.path.append("../")
from UsefulAnswerParagraphsSelection.build_entropy_set import EntropyHandler
from UsefulAnswerParagraphsSelection.entity_overlap import EntityOverLap
from UsefulAnswerParagraphsSelection.patterns import PatternHandler
from UsefulAnswerParagraphsSelection.position import PositionHandler
from RelevantQuestionRetrival.RCA import RCA
from sklearn import preprocessing
import sqlite3

class answer(object):
    def __init__(self, an,tag, sc, rel, Id):
        self.ansId = Id
        self.ans = an
        self.tags = tag
        self.score = sc
        self.relevance_score = rel
        self.entity_score = 0
        self.entropy_score = 0
        self.semantic_pattern = 0
        self.format_pattern = 0
        self.votes_score = 0
        self.overall_score = 0

class Normalize(object):

    def __init__(self):
        self.top_10 = []
        self.idf_dict = {}
        self.stopWords = []
        self.entropy = EntropyHandler()
        self.entity = EntityOverLap()
        self.pattern = PatternHandler()
        self.position = PositionHandler()

    def calculate_entropy_val(self):
        
        scores = []
        for i in range(len(self.top_10)):
            # idf_dict = self.entropy.calculate_IDF(self.top_10[i].ans)
            entropy = (self.entropy.calculate_entropy(self.stopWords, self.idf_dict, self.top_10[i].ans))
            scores.append(entropy)
            

        normalized_X = preprocessing.normalize([scores])
        to_del = []
        for i in range(len(self.top_10)):
            if normalized_X[0][i] > .1:
                self.top_10[i].entropy_score = normalized_X[0][i]
                # print(normalized_X[0][i], "****", scores[i])
            
            else:
                # print(normalized_X[0][i], "-----", scores[i])
                self.top_10[i].entropy_score = -1
            #print("Normanlized ENTROPY: {}".format(normalized_X[0][i]))

        #Delete low entropy paragraphs
        newtop = []
        for i in self.top_10:
            if i.entropy_score != -1:
                newtop.append(i)

        self.top_10 = newtop

    def normalize_relevance(self):
        rel = []
        for i in range(len(self.top_10)):
            rel.append(self.top_10[i].relevance_score)

        normalized_X = preprocessing.normalize([rel])
        for i in range(len(self.top_10)):
            self.top_10[i].relevance_score = normalized_X[0][i]
            #print("Normanlized RELEVANCE: {}".format(normalized_X[0][i]))
    
    def normalize_entity(self):
        entity = []
        for i in range(len(self.top_10)):
            x = self.entity.calc_entity(self.top_10[i].tags,self.top_10[i].ans)
            entity.append(x)

        normalized_X = preprocessing.normalize([entity]) 
        for i in range(len(self.top_10)):
            self.top_10[i].entity_score = normalized_X[0][i]
            #print("Normanlized ENTITY: {}".format(normalized_X[0][i]))
        

    def normalize_semantic_pattern(self):
        """
        docstring
        """
        semantic = []
        for i in range(len(self.top_10)):
            x = self.pattern.get_semantic_pattern_value(self.top_10[i].ans)
            self.top_10[i].semantic_pattern = x
            #print("semantic pattern: {}".format(x))
            
        

    def normalize_format_pattern(self):
        """
        docstring
        """
        for i in range(len(self.top_10)):
            x = self.pattern.get_format_pattern_value(self.top_10[i].ans)
            self.top_10[i].format_pattern = x
            #print("format pattern: {}".format(x))
    
    def normalize_votes(self):
        """
        docstring
        """
        vot = []
        for i in range(len(self.top_10)):
            vot.append(self.top_10[i].score)

        normalized_X = preprocessing.normalize([vot]) 
        for i in range(len(self.top_10)):
            self.top_10[i].votes_score = normalized_X[0][i]
            #print("Normanlized VOTES: {}".format(normalized_X[0][i]))

    def main(self, top10Q, idf_d,st):
        self.idf_dict = idf_d
        self.stopWords = st
        for i in range(len(top10Q)):
            a1 = answer(top10Q[i].ans,top10Q[i].tags, top10Q[i].ans_score,top10Q[i].Rel, top10Q[i].ansId) 
            
            self.top_10.append(a1)
        
        #query related features
        self.normalize_relevance()
        self.normalize_entity()
        #user oriented features
        self.normalize_votes()
        #paragraph
        self.calculate_entropy_val()
        self.normalize_semantic_pattern()
        self.normalize_format_pattern()

        for i in range(len(self.top_10)):
            over = self.top_10[i].relevance_score*self.top_10[i].entity_score*self.top_10[i].votes_score*self.top_10[i].entropy_score*self.top_10[i].semantic_pattern*self.top_10[i].format_pattern
            self.top_10[i].overall_score = over
            #print("ANS :{}, content:{}".format(i,self.top_10[i].ans))
            #print("OVERALL SCORE: {}".format(over))
        
        self.top_10 = sorted(self.top_10, key=lambda x: x.overall_score, reverse=True)
        return self.top_10

if __name__ == "__main__":

    a1 = answer("<p>In your example this would assign the value <code>1</code> to <code>c</code> each time.</p><p><code>cr.next()</code> is effectively equivalent to <code>cr.send(None)</code></p>")
    a2 = answer("<p>The <code>yield</code> statement used in a function turns that function into a generator (a function that creates an iterator). The resulting iterator is normally resumed by calling <code>next()</code>. However it is possible to send values to the function by calling the method <code>send()</code> instead of <code>next()</code> to resume it:</p>")
    a3 = answer("<p>What are the differences between a <a href=https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/util/HashMap.html rel=noreferrer><code>HashMap</code></a> and a <a href=https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/util/Hashtable.html rel=noreferrer><code>Hashtable</code></a> in Java?</p>\n\n<p>Which is more efficient for non-threaded applications?</p>\n")
    ans = [a1,a2,a3]
    testing = Normalize()
    testing.main(ans)
