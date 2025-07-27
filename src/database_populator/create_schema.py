import psycopg2

defaultDbName = 'gutenberg_metadata'

dbConfig = {
    'user': 'postgres',
    'host': 'localhost',
    'password': '<password>',
    'port': 5432
}

tableQueries = [
    '''CREATE TABLE records (
    id SERIAL PRIMARY KEY,
    title TEXT,
    date_of_creation VARCHAR(20),
    release_date DATE,
    description TEXT,
    url TEXT,
    bibliographic_level VARCHAR(10),
    encoding_level VARCHAR(10),
    catalog_details VARCHAR(50),
    resource_type VARCHAR(10),
    medium VARCHAR(10),
    reading_score NUMERIC(5,2),
    reading_education VARCHAR(50),
    reading_description TEXT,
    language_code VARCHAR(10),
    language_encoding VARCHAR(20),
    credits TEXT
    );
    ''',
    '''CREATE TABLE authors (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
    );
    ''',
    '''CREATE TABLE record_authors (
    record_id INT REFERENCES records(id) ON DELETE CASCADE,
    author_id INT REFERENCES authors(id) ON DELETE CASCADE,
    PRIMARY KEY (record_id, author_id)
    );
    ''',
    '''CREATE TABLE subjects (
    id SERIAL PRIMARY KEY,
    subject TEXT UNIQUE
    );
    ''',
    '''CREATE TABLE record_subjects (
    record_id INT REFERENCES records(id) ON DELETE CASCADE,
    subject_id INT REFERENCES subjects(id) ON DELETE CASCADE,
    PRIMARY KEY (record_id, subject_id)
    );  
    ''',
    '''ALTER TABLE record_authors ADD CONSTRAINT unique_record_author UNIQUE (record_id, author_id);'''
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