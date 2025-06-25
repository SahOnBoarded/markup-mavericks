import psycopg2
from lxml import etree
import time

dbName = 'gutenberg_metadata'
DATA_FILE_PATH = '<path to transformedRecords.xml>'

dbConfig = {
    'user': 'postgres',
    'host': 'localhost',
    'password': '<password>',
    'port': 5432
}

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


def writeRecordsToDb(dbName: str = None):
    if not dbName:
        print('No value entered for dbName! Aborting!')
        return
    dbConn = connectToDb(dbName)
    cursor = dbConn.cursor()
    
    tree = etree.parse(DATA_FILE_PATH)
    records = tree.xpath("//Record")

    print('Writing records to DB...')
    startTime = time.time()
    for record in records:
        
        def getText(xpathExpression):
            element = record.xpath(xpathExpression)
            return element[0].text.strip() if element and element[0].text else None

        data = {
            "title": getText("Title"),
            "date_of_creation": getText("DateOfCreation"),
            "release_date": getText("ReleaseDate"),
            "description": getText("Description"),
            "url": getText("Url"),
            "bibliographic_level": getText("Leader/BibliographicLevel"),
            "encoding_level": getText("Leader/EncodingLevel"),
            "catalog_details": getText("Leader/CatalogDetails"),
            "resource_type": getText("PhysicalDescription/ResourceType"),
            "medium": getText("PhysicalDescription/Medium"),
            "content_type": getText("ContentType/Content"),
            "content_vocab": getText("ContentType/Vocabulary"),
            "media_type": getText("MediaType/Media"),
            "media_vocab": getText("MediaType/Vocabulary"),
            "carrier_type": getText("CarrierType/Type"),
            "carrier_vocab": getText("CarrierType/Vocabulary"),
            "reading_score": getText("ReadingLevel/Score"),
            "reading_education": getText("ReadingLevel/Education"),
            "reading_description": getText("ReadingLevel/Description"),
            "language_code": getText("Language/Code"),
            "language_encoding": getText("Language/Encoding"),
            "credits": getText("Credits")
        }

        if data["reading_score"] is None:
            continue

        cursor.execute("""
            INSERT INTO records (
                title, date_of_creation, release_date, description, url,
                bibliographic_level, encoding_level, catalog_details,
                resource_type, medium, content_type, content_vocab,
                media_type, media_vocab, carrier_type, carrier_vocab,
                reading_score, reading_education, reading_description,
                language_code, language_encoding, credits
            ) VALUES (
                %(title)s, %(date_of_creation)s, %(release_date)s, %(description)s, %(url)s,
                %(bibliographic_level)s, %(encoding_level)s, %(catalog_details)s,
                %(resource_type)s, %(medium)s, %(content_type)s, %(content_vocab)s,
                %(media_type)s, %(media_vocab)s, %(carrier_type)s, %(carrier_vocab)s,
                %(reading_score)s, %(reading_education)s, %(reading_description)s,
                %(language_code)s, %(language_encoding)s, %(credits)s
            ) RETURNING id""", data)
        recordId = cursor.fetchone()[0]

        for author in record.xpath("Authors/Author"):
            name = author.text.strip()
            cursor.execute("SELECT id FROM authors WHERE name = %s", (name,))
            res = cursor.fetchone()
            if res:
                authorId = res[0]
            else:
                cursor.execute("INSERT INTO authors (name) VALUES (%s) RETURNING id", (name,))
                authorId = cursor.fetchone()[0]
            cursor.execute("INSERT INTO record_authors (record_id, author_id) VALUES (%s, %s) ON CONFLICT DO NOTHING", (recordId, authorId))

        for subj in record.xpath("Subjects/Subject"):
            subject = subj.text.strip()
            cursor.execute("SELECT id FROM subjects WHERE subject = %s", (subject,))
            res = cursor.fetchone()
            if res:
                subjectId = res[0]
            else:
                cursor.execute("INSERT INTO subjects (subject) VALUES (%s) RETURNING id", (subject,))
                subjectId = cursor.fetchone()[0]
            cursor.execute("INSERT INTO record_subjects (record_id, subject_id) VALUES (%s, %s) ON CONFLICT DO NOTHING", (recordId, subjectId))

        for subclass in record.xpath("CongressClassificationNumber/Subclass"):
            classVal = subclass.text.strip()
            cursor.execute("SELECT id FROM congress_classification WHERE class = %s", (classVal,))
            res = cursor.fetchone()
            if res:
                classId = res[0]
            else:
                cursor.execute("INSERT INTO congress_classification (class) VALUES (%s) RETURNING id", (classVal,))
                classId = cursor.fetchone()[0]
            cursor.execute("INSERT INTO record_congress_classes (record_id, class_id) VALUES (%s, %s) ON CONFLICT DO NOTHING", (recordId, classId))

    dbConn.commit()
    finishTime = time.time()
    cursor.close()
    dbConn.close()
    print("XML data writen to DB successfully in {} seconds".format((finishTime - startTime)))


writeRecordsToDb(dbName)