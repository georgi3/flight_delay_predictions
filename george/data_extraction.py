import os
import psycopg2
import pandas as pd
from src.config import DATABASE, USER, PASSWORD, HOST, PORT


def make_csv(query, filename):
    # check if file already exists
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        return df
    # ensure all columns are displayed when viewing a pandas dataframe
    pd.set_option('display.max_columns', None)
    # Creating a connection to the database
    print("creating connection...")
    con = psycopg2.connect(database=DATABASE,
                           user=USER,
                           password=PASSWORD,
                           host=HOST,
                           port=PORT)
    # creating a cursor object
    cur = con.cursor()
    # running an sql query
    print("running query...")
    cur.execute(query)
    # Storing the result
    rows = cur.fetchall()
    cols = [desc[0] for desc in cur.description]
    con.close()
    # writing the csv file
    print("writing file...")
    df = pd.DataFrame(rows, columns=cols)
    df.to_csv(filename, index=False)
    print('Done')
    return df


quer = '''SELECT t.*
FROM (
  SELECT *, row_number() OVER(ORDER BY fl_date ASC) AS row
  FROM flights
) t
WHERE t.row % 1000000 = 0'''

fname = '../data/try.csv'
make_csv(quer, fname)