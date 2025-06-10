Text Technology Project

Workflow:
A)
INPUT {XML file from the Project Gutenberg website} -> Extract relevant metadata {XML file}  -> validate against created XML schema {XSD file} -> update on postgre {   } -> query from html  {  }


OR

B)
INPUT {XML file from the Project Gutenberg website} -> JSON {xml to json converter} -> update on postgre {   } -> query from html  {  }

Usecases/research questionnaire:
One author can have multiple books written {List authors with multiple books}
One book can have multiple authors {List books with multiple authors}
One author can have multiple genre {list books of Author A with respective genre}
A book can have multiple genre references { list book with genre = history, translation} {genre = fiction, romance}
Books that are published on same date {publishing date = “..”}
Books that are released on same date {releasing date = “..”}
List books that have pages information {pages = not null}
