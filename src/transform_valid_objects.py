from saxonche import PySaxonProcessor
import os
import time

INPUT_FILE = '<put abs path to output file written after running extract_valid_objects.xml>'
OUTPUT_FILE = '<put abs path to where the output of this file would be written to>'

# This XQuery will be applied to each record
xquery = """
declare namespace marc = "http://www.loc.gov/MARC21/slim";
let $record := .
return
<Record>
  <Leader>
    <BibliographicLevel>{substring(normalize-space($record/marc:leader), 1, 3)}</BibliographicLevel>
    <EncodingLevel>{substring(normalize-space($record/marc:leader), 5, 3)}</EncodingLevel>
    <CatalogDetails>{substring(normalize-space($record/marc:leader), 9)}</CatalogDetails>
  </Leader>
  <PhysicalDescription>
    <ResourceType>{substring($record/marc:controlfield[@tag="007"], 1, 2)}</ResourceType>
    <Medium>{substring($record/marc:controlfield[@tag="007"], 4, 1)}</Medium>
  </PhysicalDescription>
  <DateOfCreation>{replace($record/marc:controlfield[@tag="008"], "r.*", "")}</DateOfCreation>
  <CongressClassificationNumber>{
    for $sub in $record/marc:datafield[@tag="050"]/marc:subfield[@code="a"]
    return <Subclass>{normalize-space($sub)}</Subclass>
  }</CongressClassificationNumber>
  <Authors>{
    for $sub in $record/marc:datafield[@tag="100"]/marc:subfield
    where not(matches($sub, '\\d'))
    return <Author>{normalize-space($sub)}</Author>
  }</Authors>
  <ContentType>
    <Content>{$record/marc:datafield[@tag="336"]/marc:subfield[@code="a"]/text()}</Content>
    <Vocabulary>{$record/marc:datafield[@tag="336"]/marc:subfield[@code="2"]/text()}</Vocabulary>
  </ContentType>
  <MediaType>
    <Media>{$record/marc:datafield[@tag="337"]/marc:subfield[@code="a"]/text()}</Media>
    <Vocabulary>{$record/marc:datafield[@tag="337"]/marc:subfield[@code="2"]/text()}</Vocabulary>
  </MediaType>
  <CarrierType>
    <Type>{$record/marc:datafield[@tag="338"]/marc:subfield[@code="a"]/text()}</Type>
    <Vocabulary>{$record/marc:datafield[@tag="338"]/marc:subfield[@code="2"]/text()}</Vocabulary>
  </CarrierType>
  {
    let $reading := (
    for $f in $record/marc:datafield[@tag="500"]
    let $s := $f/marc:subfield[@code="a"]
    where starts-with(normalize-space($s), "Reading ease score")
    return $s
  )[1]

  let $score := replace($reading, ".*score: ([0-9.]+) \\(.*", "$1")
  let $edu := replace($reading, ".*\\((.*?)\\).*", "$1")
  let $desc := replace($reading, ".*?\\)\\.\\s*", "")
  
  return <ReadingLevel>
    <Score>{$score}</Score>
    <Education>{$edu}</Education>
    <Description>{$desc}</Description>
  </ReadingLevel>
  }
  <ReleaseDate>{
    let $date := (
      for $f in $record/marc:datafield[@tag="500"]
      let $s := $f/marc:subfield[@code="a"]
      where starts-with(normalize-space($s), "Release date is")
      return $s
    )
    return replace($date, ".*?(\\d{4}-\\d{2}-\\d{2}).*", "$1")
  }</ReleaseDate>
  <Title>{
  let $title := $record/marc:datafield[@tag="245"]/marc:subfield[@code="a"]
  let $titleContinued := $record/marc:datafield[@tag="245"]/marc:subfield[@code="b"]
  let $titleStr := string-join($title, " ")
  let $titleContStr := string-join($titleContinued, " ")
  return
    if (normalize-space($titleContStr) != "")
    then concat($titleStr, " ", $titleContStr)
    else $titleStr
  }</Title>
  <Language>
      <Code>{$record/marc:datafield[@tag="041"]/marc:subfield[@code="a"]/text()}</Code>
      <Encoding>iso639-1</Encoding>
  </Language>
  <Credits>{$record/marc:datafield[@tag="508"]/marc:subfield[@code="a"]/text()}</Credits>
  <Description>{$record/marc:datafield[@tag="520"]/marc:subfield[@code="a"]/text()}</Description>
  <Subjects>{
    for $s in $record/marc:datafield[@tag="653"]/marc:subfield[@code="a"]
    return <Subject>{$s/text()}</Subject>
  }</Subjects>
  <Url>{$record/marc:datafield[@tag="856"]/marc:subfield[@code="u"]/text()}</Url>
</Record>
"""

with PySaxonProcessor(license=False) as proc:
    print('SaxonC processor initialized.')
    dom = proc.parse_xml(xml_file_name=INPUT_FILE)
    xpathProc = proc.new_xpath_processor()
    xpathProc.set_context(xdm_item=dom)
    xpathProc.declare_namespace('marc', 'http://www.loc.gov/MARC21/slim')
    recordNodes = xpathProc.evaluate('//marc:record')
    print('Found {} <record> elements.'.format(recordNodes.size))
    print('Tranforming records...')

    transformedXmlObjects = []
    startTime = time.time()
    for record in recordNodes:
        xqueryProc = proc.new_xquery_processor()
        xqueryProc.set_query_content(xquery)
        xqueryProc.set_context(xdm_item=record)
        result = xqueryProc.run_query_to_string()
        result = result.replace('<?xml version="1.0" encoding="UTF-8"?>','')
        transformedXmlObjects.append(result)

    finishTime = time.time()
    finalOutput = '<?xml version=\"1.0\" encoding=\"UTF-8\"?><Records>\n' + "\n".join(transformedXmlObjects) + '\n</Records>'

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as output:
        output.write(finalOutput)

    print('Transformation complete in {} seconds. Output written to: {}'.format((finishTime - startTime),OUTPUT_FILE))
