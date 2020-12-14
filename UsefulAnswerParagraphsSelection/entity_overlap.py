import sys
sys.path.append("../")

dict_path = "entity_set.txt"

class EntityOverLap(object):

    def load_entity_set(self):
        entity_q = set()
        for line in open(dict_path):
            line = line.strip()
            entity_q.add(line)
        return entity_q

    def calc_entity(self, E_q, E_a_q):
        inter_section = len(E_q & E_a_q)

        if len(E_q) == 0:
            result = 0
        else:
            result = inter_section / len(E_q)
        
        return result