from flask import Flask, render_template, request, jsonify
import psycopg2
import pycountry

app = Flask(__name__)

def get_connection():
    return psycopg2.connect(
        dbname='gutenberg_metadata',
        user='postgres',
        password='<password>',
        host='localhost',
        port='5432'
    )


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/unique-languages')
def get_languages():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT language_code FROM records WHERE language_code IS NOT NULL")
    rows = cur.fetchall()
    codes = [r[0] for r in rows]

    languages = [
        {"code": code, "name": pycountry.languages.get(alpha_2=code).name}
        for code in codes if pycountry.languages.get(alpha_2=code)
    ]
    languages.sort(key=lambda x: x["name"])
    return jsonify(languages)


@app.route('/subject')
def search_by_subject():
    subject_query = request.args.get('query', '').strip().lower()

    conn = get_connection()
    cur = conn.cursor()

    sql = """
        SELECT r.title, STRING_AGG(a.name, ', ') AS authors,
               r.release_date, r.reading_score as "Reading Ease Score"
        FROM records r
        JOIN record_subjects rs ON r.id = rs.record_id
        JOIN subjects s ON rs.subject_id = s.id
        JOIN record_authors ra ON r.id = ra.record_id
        JOIN authors a ON ra.author_id = a.id
        WHERE LOWER(s.subject) LIKE %s
        GROUP BY r.id
        LIMIT 20;
    """

    param = f"%{subject_query}%"
    cur.execute(sql, (param,))
    rows = cur.fetchall()

    results = []
    for row in rows:
        results.append({
            'title': row[0],
            'authors': row[1],
            'publication_date': row[2].isoformat() if row[2] else '',
            'reading_score': row[3]
        })

    cur.close()
    conn.close()
    return jsonify(results)


@app.route('/language')
def search_by_language():
    lang_query = request.args.get('query', '').strip().lower()
    
    conn = get_connection()
    cur = conn.cursor()

    sql = """
        SELECT r.title, r.reading_score as "Reading Ease Score",
               STRING_AGG(a.name, ', ') AS authors, r.release_date
        FROM records r
        JOIN record_authors ra ON r.id = ra.record_id
        JOIN authors a ON ra.author_id = a.id
        WHERE LOWER(r.language_code) = %s
        GROUP BY r.id, r.reading_score
        ORDER BY r.reading_score DESC
        LIMIT 10;
    """

    cur.execute(sql, (lang_query,))
    rows = cur.fetchall()

    results = []
    for row in rows:
        results.append({
            'title': row[0],
            'reading_score': row[1],
            'authors': row[2],
            'publication_date': row[3].isoformat() if row[3] else ''
        })

    cur.close()
    conn.close()
    return jsonify(results)

@app.route('/author')
def search_by_author():
    author_query = request.args.get('query', '').strip()
    
    print("query received: {} .".format(author_query))
    if not author_query:
        return jsonify([])

    conn = get_connection()
    cur = conn.cursor()

    sql = """
        SELECT r.title, STRING_AGG(a.name, ', ') AS authors, r.release_date, r.reading_score
FROM records r
JOIN record_authors ra ON r.id = ra.record_id
JOIN authors a ON ra.author_id = a.id
WHERE a.name ILIKE %s
GROUP BY r.id
LIMIT 20;
    """
    cur.execute(sql, (f"%{author_query}%",))
    rows = cur.fetchall()

    results = [{
        'title': row[0],
        'authors': row[1],
        'publication_date': row[2].isoformat() if row[2] else '',
        'reading_score': row[3]
    } for row in rows]

    cur.close()
    conn.close()
    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)
