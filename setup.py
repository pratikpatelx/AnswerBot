import sqlite3
from sqlite3 import Error


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

    return conn


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


def main():
    database = "pythonsqlite.db"

    sql_create_posts_table = """
    CREATE TABLE IF NOT EXISTS posts (Id INTEGER PRIMARY KEY,
        PostTypeId INTEGER,
        ParentID INTEGER,
        AcceptedAnswerId INTEGER,
        CreationDate DATETIME,
        DeletionDate DATETIME,
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


if __name__ == '__main__':
    main()

# if __name__ == "__main__":
#     conn = sqlite3.connect('example.db')
#     c = conn.cursor()

#     # Create table
#     c.execute('''CREATE TABLE stocks
#                 (date text, trans text, symbol text, qty real, price real)''')

#     # Insert a row of data
#     c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

#     # Save (commit) the changes
#     conn.commit()

#     # We can also close the connection if we are done with it.
#     # Just be sure any changes have been committed or they will be lost.
#     conn.close()
