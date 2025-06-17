Text Technology Project

Workflow:
<refer slides>

Usecases/research questionnaire:
1. One author can have multiple books written {List authors with multiple books}
-> Arthur Benjamin
SELECT * FROM books
WHERE author ILIKE '%Shakespeare%'
ORDER BY title
LIMIT 5;
2. 4. A book can have multiple genre references { list book with genre = history, translation, fiction , romance}
SELECT DISTINCT b.title
FROM books b
JOIN book_subjects s ON b.id = s.book_id
WHERE s.subject ILIKE '%Drama%'
   OR s.subject ILIKE '%History%';

3. list of books title, author and url having reading level as easy to read
SELECT b.title, a.name AS author, b.url
FROM books b
JOIN authors a ON b.id = a.book_id
WHERE b.reading_description ILIKE '%easy to read%';

4. list of books ordered by author and limit to 20 where subject has BC or BCE in it
SELECT b.title, a.name AS author, s.subject
FROM books b
JOIN authors a ON b.id = a.book_id
JOIN subjects s ON b.id = s.book_id
WHERE s.subject ILIKE '%BC%' OR s.subject ILIKE '%BCE%'
ORDER BY a.name
LIMIT 20;

5. One book can have multiple authors {List books with multiple authors}  Author count >=2
 SELECT b.title, STRING_AGG(a.name, ', ') AS authors
FROM books b
JOIN authors a ON b.id = a.book_id
GROUP BY b.id, b.title
HAVING COUNT(a.id) >= 2
ORDER BY b.title
LIMIT 100;

6. list the authors with ContentType as rdacontent, mediatype as rdamedia, carriertype as rdacarried, group them accordingly sorted by author
SELECT 
    a.name AS author,
    c.content AS content_type,
    m.media AS media_type,
    cr.type AS carrier_type
FROM authors a
JOIN books b ON a.book_id = b.id
JOIN content_type c ON b.id = c.book_id AND c.vocabulary = 'rdacontent'
JOIN media_type m ON b.id = m.book_id AND m.vocabulary = 'rdamedia'
JOIN carrier_type cr ON b.id = cr.book_id AND cr.vocabulary = 'rdacarrier'
GROUP BY a.name, c.content, m.media, cr.type
ORDER BY a.name;
