import xml.etree.ElementTree as ET

# Input and output files
xml_file = 'ebooks_full.xml'
languages_file = 'languages.txt'
output_file = 'extracted_all_output.xml'

# Read all target languages from the text file
with open(languages_file, 'r', encoding='utf-8') as f:
    target_languages = {line.strip() for line in f if line.strip()}

# Parse the XML
tree = ET.parse(xml_file)
root = tree.getroot()

# Prepare a new XML tree with a root <books>
new_root = ET.Element('books')
count = 0

# Loop through all <book> elements
for book in root.findall('.//book'):
    lang_elem = book.find('language')
    if lang_elem is not None and lang_elem.text and lang_elem.text.strip() in target_languages:
        new_root.append(book)
        count += 1

# Write the filtered books to output file
new_tree = ET.ElementTree(new_root)
new_tree.write(output_file, encoding='utf-8', xml_declaration=True)

print(f"{count} <book> entries written to {output_file}")
