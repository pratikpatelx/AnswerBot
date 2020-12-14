# pseducode for calculating entity overlap
# entities = Tag names, Tag synonymns
# identify entity mentions in a query or answer paragraph by matching words in the query or answer paragraph
# with tag names and tag synonyms
# E_q = set()
# E_a_q = set()
import sqlite3
from sqlite3 import Error
class EntityHandler(object):

    def create_connection(self):
        """ create a database connection to the SQLite database
            specified by the db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect("../pythonsqlite.db")
        except Error as e:
            print(e)

        return conn


    def select_all_tasks(self, conn):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        tags_set = set()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Posts WHERE Tags IS NOT NULL;")
        count = 0
        rows = cur.fetchall()

        for row in rows:
            #print(type(row))
            #tokenize_tags = pe.preprocess_tag(row[15])
            tags_temp = row[15].replace('<', ' ').replace('>', ' ').replace('  ', ' ').strip()
            for tag in tags_temp.split(' '):
                tags_set.add(tag)
            count += 1
            if count % 1000 ==0:
                print("Processing " + str(count))
        return tags_set

    def write_to_file(slef, filename, the_string):
        file_handler = open(filename, "w")
        file_handler.write(the_string.strip())
        file_handler.close()

    def create_dict(self):
        conn = self.create_connection()
        dict_name = "entity_set.txt"
        tags = self.select_all_tasks(conn)
        temp_str = ""
        for tag in tags:
            temp_str += (tag + "\n")
        self.write_to_file(dict_name, temp_str)
        print("Done creating the set of entities....\n")
        conn.close()
        

    def main(self):
        self.create_dict()

if __name__ == "__main__":
    entity = EntityHandler()
    entity.main()