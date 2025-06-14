import psycopg2

defaultDbName = 'gutenberg_metadata'

dbConfig = {
    'user': 'postgres',
    'host': 'localhost',
    'password': '<enter password>',
    'port': 5432
}

tableQueries = [
    '''
    CREATE TABLE records (
        id INTEGER PRIMARY KEY,
        leader TEXT,
        language TEXT,
        language_scheme TEXT,
        classification TEXT,
        release_date DATE,
        original_pub_info TEXT,
        external_url TEXT,
        summary TEXT
    );''',
    '''
    CREATE TABLE titles (
        id SERIAL PRIMARY KEY,
        record_id INTEGER REFERENCES records(id) ON DELETE CASCADE,
        title TEXT NOT NULL
    );''',
    '''
    CREATE TABLE authors (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        birth_date TEXT
    );''',
    '''
    CREATE TABLE record_authors (
        record_id INTEGER REFERENCES records(id) ON DELETE CASCADE,
        author_id INTEGER REFERENCES authors(id) ON DELETE CASCADE,
        PRIMARY KEY (record_id, author_id)
    );''',
    '''
    CREATE TABLE publishers (
        id SERIAL PRIMARY KEY,
        place TEXT,
        name TEXT,
        year TEXT
    );''',
    '''
    CREATE TABLE record_publishers (
        record_id INTEGER REFERENCES records(id) ON DELETE CASCADE,
        publisher_id INTEGER REFERENCES publishers(id) ON DELETE CASCADE,
        PRIMARY KEY (record_id, publisher_id)
    );''',
    '''
    CREATE TABLE notes (
        id SERIAL PRIMARY KEY,
        record_id INTEGER REFERENCES records(id) ON DELETE CASCADE,
        note_type TEXT,
        content TEXT
    );''',
    '''
    CREATE TABLE contributors (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL
    );''',
    '''
    CREATE TABLE record_contributors (
        record_id INTEGER REFERENCES records(id) ON DELETE CASCADE,
        contributor_id INTEGER REFERENCES contributors(id) ON DELETE CASCADE,
        PRIMARY KEY (record_id, contributor_id)
    );''',
    '''
    CREATE TABLE subjects (
        id SERIAL PRIMARY KEY,
        tag TEXT NOT NULL
    );''',
    '''
    CREATE TABLE record_subjects (
        record_id INTEGER REFERENCES records(id) ON DELETE CASCADE,
        subject_id INTEGER REFERENCES subjects(id) ON DELETE CASCADE,
        PRIMARY KEY (record_id, subject_id)
    );'''
]

'''
Function creates multiple tables based on input queries
'''
def createTables(conn, queries = [None]):
    cursor = conn.cursor()
    for query in queries:
        print('executing query: {}'.format(query))
        try:
            cursor.execute(query)
        except Exception as exp:
            print('Cannot execute query: {} ... aborting further table creation'.format(exp))
            cursor.close()
            return
    print('All tables created!')
    cursor.close()

'''
Function creates a database and closes the connection
'''
def createDb(conn, dbName: str = defaultDbName):
    cursor = conn.cursor()
    sql = 'create database {}'.format(dbName)
    try:
        cursor.execute(sql)
        print('{} database created!'.format(dbName))
    except Exception as exp:
        print('cannot create database: {}'.format(exp))
    cursor.close()
    conn.close()

'''
Function connects to a particular database and returns the connection object
'''
def connectToDb(dbName: str = None):
    if dbName:
        conn = psycopg2.connect(database = dbName,
                                user = dbConfig['user'],
                                host = dbConfig['host'],
                                password = dbConfig['password'],
                                port = dbConfig['port'])
        return conn
    else:
        print('Cannot establish connection to a database as no database specified!')


'''
Function creates the schema based on the database name and the table queries provided to it.
'''
def createSchema(dbName: str = defaultDbName, tableQueries = [None]):
    conn = connectToDb(dbName = 'postgres')
    conn.autocommit = True
    createDb(conn, dbName = dbName)
    conn = connectToDb(dbName = dbName)
    conn.autocommit = True

    if tableQueries[0]:
        createTables(conn, queries = tableQueries)
    else:
        print('No table queries given to create tables!')
        conn.close()
        return
    
    conn.close()
    print('Schema created/exists!')


createSchema(tableQueries = tableQueries)