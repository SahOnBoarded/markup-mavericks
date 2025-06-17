Text Technology Project

Workflow:
<refer slides>

Usecases/research questionnaire:
1. One author can have multiple books written {List authors with multiple books}
-> Arthur Benjamin
SELECT t.title
FROM titles t
JOIN record_authors ra ON t.record_id = ra.record_id
JOIN authors a ON ra.author_id = a.id
WHERE a.name ILIKE '%Shakespeare%'
ORDER BY t.title
LIMIT 5;

2. 4. A book can have multiple genre references { list book with genre = history, translation, fiction , romance}
SELECT DISTINCT t.title
FROM titles t
JOIN record_subjects rs ON t.record_id = rs.record_id
JOIN subjects s ON rs.subject_id = s.id
WHERE s.tag ILIKE '%History%'
   OR s.tag ILIKE '%Translation%'
   OR s.tag ILIKE '%Fiction%'
   OR s.tag ILIKE '%Romance%';

3. list of books title, author and url having reading level as easy to read
SELECT t.title, a.name AS author, r.external_url
FROM titles t
JOIN record_authors ra ON t.record_id = ra.record_id
JOIN authors a ON ra.author_id = a.id
JOIN records r ON t.record_id = r.id
JOIN record_reading_levels rrl ON r.id = rrl.record_id
JOIN reading_levels rl ON rrl.reading_level_id = rl.id
WHERE rl.description ILIKE '%easy to read%';

4. list of books ordered by author and limit to 20 where subject has BC or BCE in it
SELECT t.title, a.name AS author, s.tag AS subject
FROM titles t
JOIN record_authors ra ON t.record_id = ra.record_id
JOIN authors a ON ra.author_id = a.id
JOIN record_subjects rs ON t.record_id = rs.record_id
JOIN subjects s ON rs.subject_id = s.id
WHERE s.tag ILIKE '%BC%' OR s.tag ILIKE '%BCE%'
ORDER BY a.name
LIMIT 20;


5. One book can have multiple authors {List books with multiple authors}  Author count >=2
SELECT t.title, STRING_AGG(a.name, ', ') AS authors
FROM titles t
JOIN record_authors ra ON t.record_id = ra.record_id
JOIN authors a ON ra.author_id = a.id
GROUP BY t.record_id, t.title
HAVING COUNT(a.id) >= 2
ORDER BY t.title
LIMIT 100;

6. list the authors with ContentType as rdacontent, mediatype as rdamedia, carriertype as rdacarried, group them accordingly sorted by author
SELECT 
    a.name AS author,
    ct.content AS content_type,
    mt.media AS media_type,
    crt.type AS carrier_type
FROM authors a
JOIN record_authors ra ON a.id = ra.author_id
JOIN records r ON ra.record_id = r.id
JOIN record_content_types rct ON r.id = rct.record_id
JOIN content_types ct ON rct.content_type_id = ct.id AND ct.vocabulary = 'rdacontent'
JOIN record_media_types rmt ON r.id = rmt.record_id
JOIN media_types mt ON rmt.media_type_id = mt.id AND mt.vocabulary = 'rdamedia'
JOIN record_carrier_types rcrt ON r.id = rcrt.record_id
JOIN carrier_types crt ON rcrt.carrier_type_id = crt.id AND crt.vocabulary = 'rdacarrier'
GROUP BY a.name, ct.content, mt.media, crt.type
ORDER BY a.name;

for ebooks.xml based usecase:

1. One author can have multiple books written {List authors with multiple books}
-> Arthur Benjamin
2. One book can have multiple authors {List books with multiple authors}
 -> Author count =>2
3. One author can have multiple genre {list books of Author A with respective genre}
-> Arthur Benjamin
4. A book can have multiple genre references { list book with genre = history, translation, fiction , romance}
-> genre: History and Law
-> History and Oratory
-> Non-Fiction but not a History
5. list of countries for which books historical books are availble {genre = "history"}
6. list of countries with count of books
7. List of languages
8. author with no dates available
9. books that are translated
10. authors with date 1915
-> Klein charles and Richard Marsh
