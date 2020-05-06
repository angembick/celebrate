import boto3
import psycopg2
import os

dbname = os.environ["DB_NAME"]
user = os.environ["DB_USER"]
password = os.environ["DB_PASSWORD"]
host = os.environ["DB_HOST"]
port = os.environ["DB_PORT"]


def get_next(event, context):
    #connect to database
    conn = None
    try:
        conn = psycopg2.connect("dbname='%s' user='%s' password='%s' host='%s' port='%s' " % (dbname, user, password, host, port,))
    except:
        print("I am unable to connect to the database")
    cur = conn.cursor()  

    # get data
    cur.execute('''
        SELECT [data]
        FROM [table_name]
        WHERE [this] = [that]
        ''')

    rows = cur.fetchall()
    conn.close()
    # create message
    message = ""
    for row in rows:
        message += "🎉 " + row[0] + "💃🏽\n"

    print(message)

    s3_client = boto3.client('s3')
    try:
        s3_client.put_object(
            Bucket='[bucket_name]',
            Body=message,
            Key='bfile.txt'
            )
    except Exception as e:
        print(e)

    return

def create(event, context):
    #connect to database
    conn = None
    try:
        conn = psycopg2.connect("dbname='%s' user='%s' password='%s' host='%s' port='%s' " % (dbname, user, password, host, port,))
    except:
        print("I am unable to connect to the database")
    cur = conn.cursor()  

    #if events have record insert
    if (len(event) > 0):
        cur.execute('''
            INSERT INTO [table_name]
              ( [data])
            VALUES
              (%s);''',
              (event['[data]'])
        conn.commit()  
    else:
        print('No data received')

    conn.close()

    return

def get_all(event, context):
    #connect to database
    conn = None
    try:
        conn = psycopg2.connect("dbname='%s' user='%s' password='%s' host='%s' port='%s' " % (dbname, user, password, host, port,))
    except:
        print("I am unable to connect to the database")
    cur = conn.cursor()  

    # get bdata
    cur.execute('''
        SELECT [data]
        FROM [table_name]
        ''')

    rows = cur.fetchall()
    conn.close()
    # create message
    message = ""
    for row in rows:
        message +=  "🎉 " + row[0] + "💃🏽\n"

    print(message)
    return
