import sqlite3
import sqlite3
import os
import xml.etree.cElementTree as etree
import logging

DATASET = {
    'posts': {
        # 'ContentLicense': 'TEXT',
        'Id': 'INTEGER',
        'PostTypeId': 'INTEGER',  # 1: Question, 2: Answer
        'ParentID': 'INTEGER',  # (only present if PostTypeId is 2)
        'AcceptedAnswerId': 'INTEGER',  # (only present if PostTypeId is 1)
        'CreationDate': 'DATETIME',
        # 'DeletionDate': 'DATETIME',
        'Score': 'INTEGER',
        'ViewCount': 'INTEGER',
        'Body': 'TEXT',
        # (present only if user has not been deleted)
        'OwnerUserId': 'INTEGER',
        'OwnerDisplayName': 'TEXT',
        'LastEditorUserId': 'INTEGER',
        'LastEditorDisplayName': 'TEXT',  # ="Rich B"
        'LastEditDate': 'DATETIME',  # ="2009-03-05T22:28:34.823"
        'LastActivityDate': 'DATETIME',  # ="2009-03-11T12:51:01.480"
        'Title': 'TEXT',
        'Tags': 'TEXT',
        'AnswerCount': 'INTEGER',
        'CommentCount': 'INTEGER',
        'FavoriteCount': 'INTEGER',
        'ClosedDate': 'DATETIME',
        'CommunityOwnedDate': 'DATETIME',
        'ContentLicense': 'TEXT'
    }

    # 'votes': {
    #     'Id': 'INTEGER',
    #     'PostId': 'INTEGER',
    #     'UserId': 'INTEGER',
    #     'VoteTypeId': 'INTEGER',
    #     'CreationDate': 'DATETIME',
    #     'BountyAmount': 'INTEGER'
    # }

    # 'tags': {
    #     'Id': 'INTEGER',
    #     'TagName': 'TEXT',
    #     'Count': 'INTEGER',
    #     'ExcerptPostId': 'INTEGER',
    #     'WikiPostId': 'INTEGER'
    # }
}


# def dump_files(file_names, anathomy, dump_path='.', dump_database_name='so-dump.db', create_query='CREATE TABLE IF NOT EXISTS {table} ({fields})',
#                insert_query='INSERT INTO {table} ({columns}) VALUES ({values})',
#                log_filename='so-parser.log'):

#     logging.basicConfig(filename=os.path.join(
#         dump_path, log_filename), level=logging.INFO)
#     db = sqlite3.connect(os.path.join(dump_path, dump_database_name))
#     for file in file_names:
#         print("Opening {0}.xml").format(file)
#         with open(os.path.join(dump_path, file + '.xml')) as xml_file:
#             tree = etree.iterparse(xml_file)
#             table_name = file.lower()

#             sql_create = create_query.format(table=table_name, fields=", ".join(
#                 ['{0} {1}'.format(name, type) for name, type in anathomy[table_name].items()]))
#             print('Creating table {0}'.format(table_name))

#             try:
#                 # logging.info(sql_create)
#                 db.execute(sql_create)
#                 print("EXECUTED QUERY\n")
#             except Exception as e:
#                 logging.warning(e)

#             # TEST
#             count = 0
#             prog = 0
#             for events, row in tree:
#                 try:
#                     if row.attrib.values():
#                         logging.debug(row.attrib.keys())
#                         query = insert_query.format(table=table_name, columns=', '.join(row.attrib.keys()),
#                                                     values=('?, ' * len(row.attrib.keys()))[:-2])
#                         db.execute(query, row.attrib.values())
#                         # logging.info(query)
#                         print("EXECUTED QUERY 2\n")

#                         count += 1
#                         if (count % 1000 == 0):
#                             print("{}".format(count))

#                         if(count == 5000):
#                             print("TEST PASSED\n")
#                             break

#                 except Exception as e:
#                     logging.warning(e)
#                 finally:
#                     row.clear()

#             print("\n")
#             db.commit()
#             del (tree)


# if __name__ == '__main__':
#     dump_files(DATASET.keys(), DATASET)

def dump_files(file_names, anathomy, dump_path='.', dump_database_name='so-dump.db', create_query='CREATE TABLE IF NOT EXISTS {table} ({fields})',
               insert_query='INSERT INTO {table} ({columns}) VALUES ({values})', log_filename='so-parser.log'):
    logging.basicConfig(filename=os.path.join(
        dump_path, log_filename), level=logging.INFO)
    db = sqlite3.connect(os.path.join(dump_path, dump_database_name))
    for file in file_names:
        print("Opening {0}.xml".format(file))
        with open(os.path.join(dump_path, file + '.xml')) as xml_file:
            tree = etree.iterparse(xml_file)
            table_name = file.lower()
            for name in anathomy[table_name].items():
                print(name)

            sql_create = create_query.format(
                table=table_name,
                fields=", ".join(['{0} {1}'.format(name, type) for name, type in anathomy[table_name].items()]))

            print('Creating table {0}'.format(table_name))
            print("TESTING FIELDS>>\n")
            print(sql_create)

            try:
                logging.info(sql_create)
                db.execute(sql_create)
            except Exception as e:
                logging.warning(e)
                print(e)

            # try:
            #     print("removing tables \n")
            #     statement = "DROP TABLE [IF EXISTS] votes"
            #     db.execute(statement)
            #     statement = "DROP TABLE [IF EXISTS] tags"
            #     db.execute(statement)
            #     statement = "DROP TABLE [IF EXISTS] posts"
            #     db.execute(statement)
            #     it is failing here
            # except Exception as e:
            #     print("Failed Drop\n")
            # count = 0

            for events, row in tree:
                try:
                    if row.attrib.values():
                        logging.debug(row.attrib.keys())
                        query = insert_query.format(
                            table=table_name,
                            columns=', '.join(row.attrib.keys()),
                            values=('?, ' * len(row.attrib.keys()))[:-2])
                        # print(row.attrib.values())
                        # vals = []
                        # for key, val in row.attrib.items():
                        #     if anathomy[table_name][key] == 'INTEGER':
                        #         vals.append(int(val))
                        #     elif anathomy[table_name][key] == 'BOOLEAN':
                        #         vals.append(1 if val == "TRUE" else 0)
                        #     else:
                        #         vals.append(val)
                        db.execute(query, row.attrib.values())

                        count += 1
                        if (count % 1000 == 0):
                            print("{}".format(count))

                            if(count == 5000):
                                print("TEST PASSED\n")
                                break

                except Exception as e:
                    logging.warning(e)
                    print(e)
                finally:
                    row.clear()
            print("\n")
            db.commit()
            del (tree)


if __name__ == '__main__':
    dump_files(DATASET.keys(), DATASET)
