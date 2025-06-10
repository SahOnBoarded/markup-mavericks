import xml.etree.ElementTree as ET

# Input and output file names
xml_file = 'ebooks_full.xml'
output_file = 'xml_output.xml'

# Load and parse the XML file
tree = ET.parse(xml_file)
root = tree.getroot()

# Define languages to filter
target_languages = {'de', 'nl'}

# Store matching <book> elements
filtered_books = []

# Loop over all <book> elements
for book in root.findall('.//book'):
    lang_elem = book.find('language')
    if lang_elem is not None and lang_elem.text and lang_elem.text.strip() in target_languages:
        filtered_books.append(book)

# Create new root for output XML
new_root = ET.Element('books')

# Append the matching books
for b in filtered_books:
    new_root.append(b)

# Build the new XML tree and write to file
new_tree = ET.ElementTree(new_root)
new_tree.write(output_file, encoding='utf-8', xml_declaration=True)

print(f"Filtered {len(filtered_books)} books into {output_file}")
