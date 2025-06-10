Text Technology Project

Workflow:
A)
INPUT {XML file from the Project Gutenberg website} -> Extract relevant metadata {XML file}  -> 
validate against created XML schema {XSD file} -> update on postgre {   } -> query from html  {  }


OR

B)
INPUT {XML file from the Project Gutenberg website} -> JSON {xml to json converter} -> 
update on postgre {   } -> query from html  {  }

Usecases/research questionnaire:
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
6. list of countries and their count of books
7. List of languages
8. authors with no dates available
-> 
9. books that are translated
-> genre = Translation
10. authors with date 1915
-> Klein charles and Richard Marsh
11. list of books having languages more than one
-> af;nl
-> en; la; el
12. author lastnames with first name as "Arthur"
-> Arthur Benjamin and Arthur Hornblow
13. list of genre availble
14. books with no author information
15. authors of dates BC|AD

