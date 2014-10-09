from xml.dom import minidom
import json
import urllib2
import re
from os import listdir, unlink
from os.path import isfile, join
from random import randrange
from time import sleep
from xml.parsers import expat

def main():
    yearsi = range(2002,2013)
    input_files = ['iswcs','ew','wowmom','wcnc','vtc_spring','vtc_fall','icc',
                   'globecom','pimrc','jsac','tvt','twc','letters']
    
    app_id = json.loads(open('settings.json').read())['app_id']
    
    input_dir = 'raw-data'
    output_dir = 'processed-data'
    
    for file in input_files:
        for yeari in yearsi:
            data = []
            year = str(yeari)
            input_file = input_dir + '/' + file + '_' + year + '.xml'
            output_file = output_dir + '/' + file + '_' + year + '.json'
            process_raw_data(input_file,output_file,year,data,app_id)
        
            print('Saving Output File: ' + output_file + '\n')
            with open(output_file,'w') as f:
                json.dump(data,f)   
        

def process_raw_data(input_file,output_file,year,data,app_id):
    print('Processing File: ' + input_file)
    
    try:
        xmldoc = minidom.parse(input_file)
        documents = xmldoc.getElementsByTagName('document')
    
        count = 0
        for document in documents:
            count += 1
            title = get_tag(document,'title')        
            authors = get_tag(document,'authors')
            affiliations = get_tag(document,'affiliations')
            doi = get_tag(document,'doi')
            issn = get_tag(document,'issn')
            pdf = get_tag(document,'pdf')

            tags = []
            controlled_terms = document.getElementsByTagName('controlledterms')
            for controlled_term in controlled_terms:
                terms = controlled_term.getElementsByTagName('term')
                for term in terms:
                    tags.append(term.childNodes[0].data)
    
            thesaurus_terms = document.getElementsByTagName('thesaurusterms')
            for thesaurus_term in thesaurus_terms:
                terms = thesaurus_term.getElementsByTagName('term')
                for term in terms:
                    tags.append(term.childNodes[0].data)

            tags = ','.join(tags)

            citations = 0
            if len(authors) > 0:
                query_title = title
                if ':' in query_title and query_title.index(':') == 7:
                    query_title = query_title[8:].lstrip()
            
                # Throttle queries and limit to 200 queries per minute
                if count >= 200:
                    print '\nThrottling queries...\n'
                    sleep(60)
                    count = 0
                
                print 'Obtaining Citations for DOI = ' + doi
                citations = get_citations(app_id,query_title)
                print 'Citations = ' + str(citations)
        
            dict = {'title':title,
                    'authors':authors,
                    'affiliations':affiliations,
                    'doi':doi,
                    'issn':issn,
                    'pdf':pdf,
                    'tags':tags,
                    'citations':citations,
                    'year':year}
                
            data.append(dict)
    except Exception, e:
        print e

def get_tag(document,tag_name):
    value = ''
    tag_x = document.getElementsByTagName(tag_name)
    if len(tag_x) > 0:
        tag_x_c = tag_x[0].childNodes
        if len(tag_x_c) > 0:
            value = tag_x_c[0].data
    return value

def clear_output_dir(output_dir):
    output_files = [ f for f in listdir(output_dir) if isfile(join(output_dir,f)) ]
    for output_file in output_files:
        try:
            unlink(join(output_dir,output_file))
        except Exception, e:
            print e

def get_citations(app_id,title):
    query_start = 'http://academic.research.microsoft.com/json.svc/search?AppId=' + app_id + '&TitleQuery='
    title_query = title.replace(' ','+')
    query_end = '&ResultObjects=Publication&PublicationContent=AllInfo&StartIdx=1&EndIdx=1'
    url_title = query_start + title_query + query_end
    
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}

    try:
        request = urllib2.Request(url_title,None,hdr)
        response = urllib2.urlopen(request)
    
        data = json.load(response)
    
        return extract_citations_from_data(data)
    except Exception, e:
        print e, title

    return -1

def extract_citations_from_data(data):
    if 'd' in data:
        d = data['d']
        if 'Publication' in d:
            publication = d['Publication']
            if 'Result' in publication:
                result = publication['Result']
                if len(result) > 0:
                    result = result[0]
                    if 'CitationCount' in result:
                        return result['CitationCount']

    return -1

if __name__ == "__main__":
    main()
    # https://www.maxmind.com/en/worldcities