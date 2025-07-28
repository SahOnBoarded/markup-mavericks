# Text Technology Project: Project Gutenberg 

## Team Members:

- Aldrin Joe (3697300)
- Sahana Korody Manjunatha (3698008)
- Vedant Puranik (3703786)

## Steps to run the Collect-Prepare-Access phases

### Collect

1. Unzip the file **pgmarc.zip** inside the `resources/xml` folder and place the contained file in a location of your choice (preferrably inside the same folder `resources/xml` for convenience).

**Note**: We downloaded the original file "pgmarc.xml" from Project Gutenberg's official feeds [page](https://www.gutenberg.org/cache/epub/feeds/) as mentioned on their [official page](https://www.gutenberg.org/ebooks/offline_catalogs.html#:~:text=very%20user%2Dfriendly.-,The%20Project%20Gutenberg%20Catalog%20Metadata%20in%20Machine%2DReadable%20Format,-XML/RDF/CSV), fully abiding to their [usage policy](https://www.gutenberg.org/policy/robot_access.html). This file is regularly updated by their team and these updates also involve schema changes which would require corresponding changes to the program. Hence, for practial purposes, the file we used while developing this project (mid-June) has been added in the `resources/xml` folder. 

### Prepare

**NOTE**: If using a Windows system, when entering the paths, use a `\\` instead of a `\` for folder separations e.g. "C:`\\`Vedant`\\`Uni`\\`Subjects`\\`TT`\\`markup-maverics`\\`src" instead of "C:\Vedant\Uni\Subjects\TT\markup-maverics\src" 

1. Ensure you have placed the pgmarc.xml file in a place you know.
2. Ensure you have all python dependencies installed:
    - Change directory to `src/`
    - Run `pip install -r requirements.txt`
3. Edit `src/extract_valid_objects.py` and set the values of: 
    - `XML_PATH`: Absolute path of pgmarc.xml on your local system.
    - `XSD_PATH`: Absolute path of `resources/record_schema.xsd` on your local system.
    - `OUTPUT_PATH`: Absolute path of the output file (including the name of the file and .xml extension e.g. "path/extractedObjects.xml") that would be created on your local system and will store results of this program.
4. Edit `src/transform_valid_objects.py` and set the values of:
    - `INPUT_FILE`: Same as the `OUTPUT_PATH` from the previous step.
    - `OUTPUT_FILE`: Absolute path of the output file (including the name of the file and .xml extension e.g. "path/transformedObjects.xml") that would be created on your local system and will store results of this program.
5. Edit `src/database_populator/create_schema.py` and set the values of:
    - `dbConfig['password']`: Enter password of your local PostgreSQL setup.
    - Change other fields in the `dbConfig` object if you must to get access to the user 'postgres' inside your PostgreSQL server.
6. Edit `src/database_populator/write_records.py` and set the values of:
    - `dbConfig['password']`: Enter password of your local PostgreSQL setup.
    - `DATA_FILE_PATH`: Same as the value of `OUTPUT_FILE` from step 4.
7. Don't change anything else to ensure the program works correctly.
8. Run all 4 Python scripts in **this order**:
    - `python src/extract_valid_objects.py`
    - `python src/transform_valid_objects.py`
    - `python src/database_populator/create_schema.py`
    - `python src/database_populator/write_records.py`
9. After this all of the data should be in your postgres server inside the database called `gutenberg_metadata`. To verify, simply connect to the database using your console or pgadmin, and run `select count(*) from records;`, this should show you a non-zero value (typically more than 25000) which would confirm successful data insertion.

### Access

1. Edit `src/flask-app/app.py`:
    - Add your postgres password for the value inside psycopg2.connect() function call (line 11).
2. Run `python src/flask_app/app.py` to start the Flask server.
3. Open http://127.0.0.1:5000 in your browser.
4. All data is served through this HTML interface.