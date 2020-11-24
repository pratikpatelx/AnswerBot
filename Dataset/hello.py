import sqlite3
import os
import xml.etree.cElementTree as etree
import logging

ANATHOMY = {
#   'posts': {
#       'Id': 'INTEGER',
#       'PostTypeId': 'INTEGER',  # 1: Question, 2: Answer
#       'ParentId': 'INTEGER',  # (only present if PostTypeId is 2)
#       'AcceptedAnswerId': 'INTEGER',  # (only present if PostTypeId is 1)
#       'CreationDate': 'DATETIME',
#       'Score': 'INTEGER',
#       'ViewCount': 'INTEGER',
#       'Body': 'TEXT',
#       'OwnerUserId': 'INTEGER',  # (present only if user has not been deleted)
#       'OwnerDisplayName': 'TEXT',
#       'LastEditorUserId': 'INTEGER',
#       'LastEditorDisplayName': 'TEXT',  # ="Rich B"
#       'LastEditDate': 'DATETIME',  #="2009-03-05T22:28:34.823"
#       'LastActivityDate': 'DATETIME',  #="2009-03-11T12:51:01.480"
#       'CommunityOwnedDate': 'DATETIME',  #(present only if post is community wikied)
#       'Title': 'TEXT',
#       'Tags': 'TEXT',
#       'AnswerCount': 'INTEGER',
#       'CommentCount': 'INTEGER',
#       'FavoriteCount': 'INTEGER',
#       'ClosedDate': 'DATETIME'
#   },
#   'votes': {
#       'Id': 'INTEGER',
#       'PostId': 'INTEGER',
#       'UserId': 'INTEGER',
#       'VoteTypeId': 'INTEGER',
#       # -   1: AcceptedByOriginator
#       # -   2: UpMod
#       # -   3: DownMod
#       # -   4: Offensive
#       # -   5: Favorite
#       # -   6: Close
#       # -   7: Reopen
#       # -   8: BountyStart
#       # -   9: BountyClose
#       # -  10: Deletion
#       # -  11: Undeletion
#       # -  12: Spam
#       # -  13: InformModerator
#       'CreationDate': 'DATETIME',
#       'BountyAmount': 'INTEGER'
#   },

  'tags': {
      'Id': 'INTEGER',
      'TagName': 'TEXT',
      'Count': 'INTEGER',
      'ExcerptPostId': 'INTEGER',
      'WikiPostId': 'INTEGER'
  }
}


def dump_files(file_names, anathomy,
             dump_path='.',
             dump_database_name='so-dump.db',
             create_query='CREATE TABLE IF NOT EXISTS {table} ({fields})',
             insert_query='INSERT INTO {table} ({columns}) VALUES ({values})',
             log_filename='so-parser.log'):
  logging.basicConfig(filename=os.path.join(dump_path, log_filename), level=logging.INFO)
  db = sqlite3.connect(os.path.join(dump_path, dump_database_name))
  for file in file_names:
      print("Opening {0}.xml".format(file))
      with open(os.path.join(dump_path, file + '.xml')) as xml_file:
          tree = etree.iterparse(xml_file)
          table_name = file.lower()

          sql_create = create_query.format(
              table=table_name,
              fields=", ".join(['{0} {1}'.format(name, type) for name, type in anathomy[table_name].items()]))
          print('Creating table {0}'.format(table_name))

          try:
              logging.info(sql_create)
              db.execute(sql_create)
          except Exception as e:
              logging.warning(e)

          count = 0
          for events, row in tree:
              try:
                  if row.attrib.values():
                      logging.debug(row.attrib.keys())
                      query = insert_query.format(
                          table=table_name,
                          columns=', '.join(row.attrib.keys()),
                          values=('?, ' * len(row.attrib.keys()))[:-2])
                      vals = []
                      for key, val in row.attrib.items():
                          if anathomy[table_name][key] == 'INTEGER':
                              vals.append(int(val))
                          elif anathomy[table_name][key] == 'BOOLEAN':
                              vals.append(1 if val=="TRUE" else 0)
                          else:
                              vals.append(val)
                      db.execute(query, vals)

                      count += 1
                      if (count % 1000 == 0):
                          print("{}".format(count))

              except Exception as e:
                  logging.warning(e)
                  print("x")
              finally:
                  row.clear()
          print("\n")
          db.commit()
          del (tree)


if __name__ == '__main__':
  dump_files(ANATHOMY.keys(), ANATHOMY)