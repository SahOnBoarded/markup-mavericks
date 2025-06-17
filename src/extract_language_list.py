import xml.etree.ElementTree as ET

# Path to your XML file
xml_file = 'ebooks_full.xml'
output_file = 'languages.txt'

# Parse the XML
tree = ET.parse(xml_file)
root = tree.getroot()

# Collect language values
languages = set()  # Use set to avoid duplicates

# Adjust this if <language> elements are deeply nested or have namespaces
for language in root.iter('language'):
    if language.text:
        languages.add(language.text.strip())

# Write to a text file
with open(output_file, 'w', encoding='utf-8') as f:
    for lang in sorted(languages):
        f.write(lang + '\n')

print(f"{len(languages)} unique language(s) written to {output_file}")
