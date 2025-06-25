# Research Question Queries

# What are some books related to a particular subject?

```sql
SELECT r.title, STRING_AGG(DISTINCT a.name, ' ') AS authors, r.release_date, r.reading_score as "Reading Ease Score"
FROM records r
JOIN record_subjects rs ON r.id = rs.record_id
JOIN subjects s ON rs.subject_id = s.id
JOIN record_authors ra ON r.id = ra.record_id
JOIN authors a ON ra.author_id = a.id
WHERE LOWER(s.subject) LIKE %s
GROUP BY r.id
LIMIT 20;
```

# What are the top 10 easiest to read books from a particular language?

```sql
SELECT r.title, r.reading_score as "Reading Ease Score", STRING_AGG(a.name, ' ') AS authors, r.release_date
FROM records r
JOIN record_authors ra ON r.id = ra.record_id
JOIN authors a ON ra.author_id = a.id
WHERE LOWER(r.language_code) = %s
GROUP BY r.id, r.reading_score
ORDER BY r.reading_score DESC
LIMIT 10;
```

# Search for books by author name

```sql
SELECT r.title, STRING_AGG(a.name, ' ') AS authors, r.release_date, r.reading_score
FROM records r
JOIN record_authors ra ON r.id = ra.record_id
JOIN authors a ON ra.author_id = a.id
WHERE a.name ILIKE %s
GROUP BY r.id
LIMIT 20;
```