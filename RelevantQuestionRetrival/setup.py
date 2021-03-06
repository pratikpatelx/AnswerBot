import sqlite3
from sqlite3 import Error
import xml.etree.ElementTree as ET
import sys
sys.path.append("../")

# import lxml as etree


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)


def close_connection(conn):
    """
    close a database connection to the SQLite database
    :param conn: Connection object
    :return:
    """
    conn.close()


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def insert_data(conn, fileName, tab):
    # Path should be a relative path from your pc
    # insert posts
    tree = ET.parse(fileName)
    root = tree.getroot()
    curs = conn.cursor()
    # root = ET.tostring(root, encoding='utf8').decode('utf8')
    print("Root of the table is at ", root)
    count = 0
    insert_query = "INSERT INTO {table} ({columns}) VALUES ({values});"
    for child in root:
        val = ""

        for i in range(len(child.attrib.values()) - 1):
            val = val + "?, "

        val = val + "?"
        query = insert_query.format(table=tab, columns=', '.join(child.attrib.keys()), values=val)
        vac = []
        for i in child.attrib.values():
            vac.append(i)
        curs.execute(query, vac)
        count = count +1
        conn.commit()
    print("\n --------------------------------------------------------------------------------------------")
    print("Done Inserting into", tab, "Count: ", count)
    print("\n --------------------------------------------------------------------------------------------\n\n")
    del (tree)
    # inserting data to the DB


def main():
    database = "../pythonsqlite.db"

    sql_create_posts_table = """
    CREATE TABLE IF NOT EXISTS Posts (Id INTEGER PRIMARY KEY,
        PostTypeId INTEGER,
        ParentID INTEGER,
        AcceptedAnswerId INTEGER,
        CreationDate DATETIME,
        Score INTEGER,
        ViewCount INTEGER,
        Body TEXT,
        OwnerUserId INTEGER, 
        OwnerDisplayName TEXT,
        LastEditorUserId INTEGER,
        LastEditorDisplayName TEXT,
        LastEditDate DATETIME,
        LastActivityDate DATETIME,
        Title TEXT,
        Tags TEXT,
        AnswerCount INTEGER,
        CommentCount INTEGER,
        FavoriteCount INTEGER,
        ClosedDate DATETIME,
        CommunityOwnedDate DATETIME,
        ContentLicense TEXT
        );"""
    sql_create_votes_table = """
    CREATE TABLE IF NOT EXISTS Votes(
        Id INTEGER,
        PostId INTEGER,
        UserId INTEGER,
        VoteTypeId INTEGER,
        CreationDate DATETIME,
        BountyAmount INTEGER
    );"""
    
    sql_create_tags_table = """
    CREATE TABLE IF NOT EXISTS Tags(
        Id INTEGER,
        TagName TEXT,
        Count INTEGER,
        ExcerptPostId INTEGER,
        WikiPostId INTEGER
    );"""

    conn = create_connection(database)

    if conn is not None:
        # create_table(conn, sql_create_posts_table)
        # create_table(conn, sql_create_votes_table)
        create_table(conn, sql_create_tags_table)

    else:
        print("..Error creating tables for DB..\n")

    print("Please wait...... BULK inserting data into Table Posts...\n")
    insert_data(conn, 'Posts.xml', "Posts")

    print("Please wait...... BULK inserting data into Table Votes..\n")
    insert_data(conn, 'Votes.xml', "Votes")
    print("Please wait...... BULK inserting data into Table Tags..\n")
    insert_data(conn, 'tags.xml', "Tags")
    print("DONE data insertion.... Closing DB...\n")
    close_connection(conn)


if __name__ == '__main__':
    main()
