import os
from lxml import etree
import time

XML_PATH = '<put abs path to pgmarc.xml>'
XSD_PATH = '<put abs path to record_schema.xsd>'
OUTPUT_PATH = '<put output path where the output file would be written to>'

NSMAP = {'marc': 'http://www.loc.gov/MARC21/slim'} # This is the MARC21 namespace used in the file pgmarc.xml.

def validateAndExtractRecords(xmlPath, xsdPath, outputPath):
    print('Extracting valid records...')
    with open(xsdPath, 'rb') as f:
        schema_doc = etree.parse(f)
        schema = etree.XMLSchema(schema_doc)

    doc = etree.parse(xmlPath)
    root = doc.getroot()

    newRoot = etree.Element("{http://www.loc.gov/MARC21/slim}collection", nsmap=root.nsmap)

    startTime = time.time()
    # Extract and validate each <record>
    for record in root.findall('marc:record', namespaces=NSMAP):
    # We filter out all records before the year 2015 to keep the output size smaller. 
    # This step could be altered or removed to change the size of the output dataset.
        valid = False
        for df in record.findall('marc:datafield', namespaces=NSMAP):
            if df.attrib.get('tag') == '264' and df.attrib.get('ind1') == ' ' and df.attrib.get('ind2') == '1':
                for sf in df.findall('marc:subfield', namespaces=NSMAP):
                    if sf.attrib.get('code') == 'c':
                        try:
                            year = int(''.join(filter(str.isdigit, sf.text or '')))
                            if year > 2015:
                                valid = True
                        except ValueError:
                            pass
        if valid:
            intermediateCollection = etree.Element("{http://www.loc.gov/MARC21/slim}collection", nsmap=root.nsmap)
            intermediateCollection.append(record)
            try:
                schema.assertValid(etree.ElementTree(intermediateCollection))
                newRoot.append(etree.fromstring(etree.tostring(record)))
            except etree.DocumentInvalid:
                continue

    finishTime = time.time()
    print('Total time taken to process all objects = {} seconds'.format(finishTime - startTime))
    
    # Write the filtered output to the file specified by OUTPUT_PATH
    newTree = etree.ElementTree(newRoot)
    newTree.write(outputPath, pretty_print=True, encoding='UTF-8', xml_declaration=True)
    print('Valid objects written to {}'.format(OUTPUT_PATH))


validateAndExtractRecords(XML_PATH, XSD_PATH, OUTPUT_PATH)