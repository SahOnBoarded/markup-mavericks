import xmltodict
import json

# Load your XML file
with open("ebooks.xml", "r", encoding="utf-8") as xml_file:
    xml_data = xml_file.read()

# Parse and convert to JSON
json_data = json.dumps(xmltodict.parse(xml_data), indent=2)

# Write JSON to a file
with open("ebooks.json", "w", encoding="utf-8") as json_file:
    json_file.write(json_data)

print("Conversion complete! JSON saved as ebooks.json")
