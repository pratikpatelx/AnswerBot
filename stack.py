import sqlite3
import os
import xml.etree.cElementTree as etree
import logging

ANATHOMY = {

    # 'comments': {
    #     'Id': 'INTEGER',
    #     'PostId': 'INTEGER',
    #     'Score': 'INTEGER',
    #     'Text': 'TEXT',
    #     'CreationDate': 'DATETIME',
    #     'UserId': 'INTEGER',
    #     'UserDisplayName': 'TEXT'
    # },


    # 'posthistory': {
    #     'Id': 'INTEGER',
    #     'PostHistoryTypeId': 'INTEGER',
    #     'PostId': 'INTEGER',
    #     'RevisionGUID': 'INTEGER',
    #     'CreationDate': 'DATETIME',
    #     'UserId': 'INTEGER',
    #     'UserDisplayName': 'TEXT',
    #     'Comment': 'TEXT',
    #     'Text': 'TEXT'
    # },
    # 'postlinks': {
    #     'Id': 'INTEGER',
    #     'CreationDate': 'DATETIME',
    #     'PostId': 'INTEGER',
    #     'RelatedPostId': 'INTEGER',
    #     'PostLinkTypeId': 'INTEGER',
    #     'LinkTypeId': 'INTEGER'
    # },
    # 'users': {
    #     'Id': 'INTEGER',
    #     'Reputation': 'INTEGER',
    #     'CreationDate': 'DATETIME',
    #     'DisplayName': 'TEXT',
    #     'LastAccessDate': 'DATETIME',
    #     'WebsiteUrl': 'TEXT',
    #     'Location': 'TEXT',
    #     'Age': 'INTEGER',
    #     'AboutMe': 'TEXT',
    #     'Views': 'INTEGER',
    #     'UpVotes': 'INTEGER',
    #     'DownVotes': 'INTEGER',
    #     'EmailHash': 'TEXT',
    #     'AccountId': 'INTEGER',
    #     'ProfileImageUrl': 'TEXT'
    # },

}


def dump_files(file_names, anathomy,
               dump_path='.',
               dump_database_name='so-dump.db',
               create_query='CREATE TABLE IF NOT EXISTS {table} ({fields})',
               insert_query='INSERT INTO {table} ({columns}) VALUES ({values})',
               log_filename='so-parser.log'):
    logging.basicConfig(filename=os.path.join(
        dump_path, log_filename), level=logging.INFO)
    db = sqlite3.connect(os.path.join(dump_path, dump_database_name))
    for file in file_names:
        print("Opening {0}.xml".format(file))
        with open(os.path.join(dump_path, file + '.xml')) as xml_file:
            tree = etree.iterparse(xml_file)
            table_name = file

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
                        db.execute(query, row.attrib.values())
                        # print ".",
                except Exception as e:
                    logging.warning(e)
                    # print "x",
                finally:
                    row.clear()

                # Do you need this???????
                count = count + 1
                if count == 10000:
                    print("-3-")
                    count = 0

            # print "\n"
            db.commit()
            del (tree)


if __name__ == '__main__':
    dump_files(ANATHOMY.keys(), ANATHOMY)
