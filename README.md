# Project Gutenberg : Text Technology

## Team Members:

- Aldrin Joe
- Sahana Korody Manjunatha
- Vedant Puranik

## Steps to run the Collect-Prepare-Access phases

### Collect

1. Download the **pgmarc.xml** file from Project Gutenberg: [link](https://www.gutenberg.org/cache/epub/feeds/) as mentioned on their [official page](https://www.gutenberg.org/ebooks/offline_catalogs.html#:~:text=very%20user%2Dfriendly.-,The%20Project%20Gutenberg%20Catalog%20Metadata%20in%20Machine%2DReadable%20Format,-XML/RDF/CSV). We need to download this in accordance to their [policy](https://www.gutenberg.org/policy/robot_access.html) against any other kind of robotic access.

2. Place the downloaded file preferrably inside resources/xml folder (create an empty xml folder inside resources). This is just a recommendation, you are free to put it anywhere in your system.

### Prepare

1. Ensure you have placed the pgmarc.xml file in a place you know.
2. Ensure you have all python dependencies installed:
    - Change directory to `src/`
    - Run `pip install -r requirements.txt`
2. Edit `src/extract_valid_objects.py`: 
    - `XML_PATH`: Absolute path of pgmarc.xml on your local system.
    - `XSD_PATH`: Absolute path of `resources/record_schema.xsd` on your local system.
    - `OUTPUT_PATH`: Absolute path of the output file (including the name of the file and .xml extension) on your local system that will store results of this program.
3. Edit `src/transform_valid_objects.py`:
    - `INPUT_FILE`: Same as the `OUTPUT_PATH` from the previous step.
    - `OUTPUT_FILE`: Absolute path of the output file (including the name of the file and .xml extension) on your local system that will store results of this program.
4. Edit `src/database_populator/create_schema.py`:
    - `dbConfig['password']`: Enter password of your local PostgreSQL setup.
    - Change other fields if you must to get access to the user 'postgres' inside PostgreSQL server.
5. Edit `src/database_populator/write_records.py`:
    - `dbConfig['password']`: Enter password of your local PostgreSQL setup.
    - `DATA_FILE_PATH`: Same as the value of `OUTPUT_FILE` from step 3.
7. Don't change anything else to ensure the program works correctly.
8. Run all 4 Python scripts in this order:
    - `src/extract_valid_objects.py`
    - `src/transform_valid_objects.py`
    - `src/database_populator/create_schema.py`
    - `src/database_populator/write_records.py`
9. After this all of the data should be in your postgres server inside the database called `gutenberg_metadata`. To verify, simply connect to the database using your console or pgadmin, and run `select count(*) from records;`, this should show you a non-zero value (typically more than 25000) which would confirm successful data insertion.

### Access

1. Edit `src/flask-app/app.py`:
    - Add your postgres password for the value inside psycopg2.connect() function call (line 11).
2. Run `python app.py` to start the Flask server.
3. Open http://127.0.0.1:5000 in your browser.
4. All data is served through this HTML interface.