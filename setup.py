import sqlite3
from sqlite3 import Error
import xml.etree.ElementTree as ET
import lxml as etree


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


def insert_data(conn):
    # Path should be a relative path from your pc
    # parser = etree.XMLParser(recover=true)
    # root = etree.XML('smallP.xml')
    tree = ET.parse('smallP.xml')
    root = tree.getroot()
    curs = conn.cursor()
    #root = ET.tostring(root, encoding='utf8').decode('utf8')
    print("root of the posts is ", root)
    count = 0
    insert_query = "INSERT INTO {table} ({columns}) VALUES ({values});"
    for child in root:
        val = ""

        for i in range(len(child.attrib.values())-1):
            val = val + "?, "

        print(len(child.attrib.keys()), "--------------",
              len(child.attrib.values()))
        val = val + "?"
        query = insert_query.format(table="posts", columns=', '.join(
            child.attrib.keys()), values=val)

        curs.execute(query, child.attrib.values())

        conn.commit()
        count = count + 1
        if count > 1000:
            break


def main():
    database = "pythonsqlite.db"

    sql_create_posts_table = """
    CREATE TABLE IF NOT EXISTS posts (Id INTEGER PRIMARY KEY,
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

    conn = create_connection(database)

    if conn is not None:
        # create projects table
        create_table(conn, sql_create_posts_table)

    else:
        print("Error! cannot create the database connection.")

    insert_data(conn)

    close_connection(conn)


if __name__ == '__main__':
    main()
