import MySQLdb


PASS = ''


def commit(query):
    # Open database connection
    db = MySQLdb.connect('127.0.0.1', 'root', PASS, 'video')

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # execute SQL query using execute() method.
    cursor.execute(query)
    db.commit()

    # disconnect from server
    db.close()


def fetch_all(query):
    # Open database connection
    db = MySQLdb.connect('127.0.0.1', 'root', PASS, 'video')

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # execute SQL query using execute() method.
    cursor.execute(query)
    result = cursor.fetchall()

    # disconnect from server
    db.close()

    return result
