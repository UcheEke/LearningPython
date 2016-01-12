import sqlite3


def create_table(cur, table_name, **kwargs):
    """
    Creates a table based on a dictionary of values
    :param cur: cursor to an open database connection
    :param table_name: name of the table to be created
    :param kwargs: optional table creation keyword variables
    :return: none
    """
    kcount = 0
    sql = "CREATE TABLE " + table_name + "("

    for k, v in kwargs.items():
        kcount += 1
        sql += k + " " + v + " "
        if kcount < len(kwargs.keys()):
            sql += ","
    sql += ")"

    cur.execute(sql)


def enter_data(cur, table_name, cmd, **kwargs):
    """
    Uses SQL command cmd to enter columnar data in to database table, table_name
    :param cur: cursor to an open database connection
    :param table_name: name of table to be altered
    :param cmd: SQL command to pass to the table
    :param kwargs: optional keyword arguments for SQL command cmd
    :return:
    """
    sql = cmd + " INTO " + table_name + " ("
    kcount = 0
    for k, _ in kwargs.items():
        kcount += 1
        sql += str(k)
        if kcount < len(kwargs.keys()):
            sql += ","

    sql += ") VALUES ("

    for i in range(kcount-1):
        sql += "?,"

    sql += "?)"

    values = tuple([v for _, v in kwargs.items()])
    cur.execute(sql, values)


def yes_no(prompt):
    response = input("{} [Y/N]".format(prompt)).strip().lower()
    if response == 'y':
        return True
    else:
        return False


if __name__ == '__main__':
    schema = {'name': "TEXT", 'age': "INTEGER", 'comment': "TEXT"}

    # Define a few datapoints in keeping with the schema
    dp1 = {'name': 'Uche', 'age': 44, 'comment': 'This is a test!'}
    dp2 = {'name': 'Francis', 'age': 42, 'comment': "This isn't a test!"}
    dp3 = {'name': 'Linda', 'age': 39, 'comment': "It's always a test"}
    dp4 = {'name': 'Jenn', 'age': 48, 'comment': "It's never a test"}

    # Establish a connection within a context manager
    with sqlite3.connect('tutorial.db') as conn:
        cursor = conn.cursor()
        # delete the old table
        cursor.execute("DROP TABLE IF EXISTS PEOPLE")
        create_table(cursor, 'PEOPLE', **schema)
        for datapoint in [dp1, dp2, dp3, dp4]:
            enter_data(cursor, 'PEOPLE', "INSERT", **datapoint)
            conn.commit()

        # read the data back with a user provided SQL query
        while True:
            query = input("Enter your SQL query: ").rstrip()
            print("You entered: {}".format(query))
            if not yes_no("Proceed?"):
                break
            else:
                for row in cursor.execute(query):
                    print(row)

            if not yes_no("Perform another SQL query?"):
                break
