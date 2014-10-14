import json
import urllib2
import re
import zipfile
import shutil
import csv
from xml.dom import minidom
from os import listdir, unlink, remove
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
    location_data_dir = 'location-data'
    location_data_file = 'worldcitiespop.txt'
    country_codes_file = 'country_codes.csv'
    
    regions = {}
    country_codes = {}
    countries = {}
    
    print 'Extracting location data...'
    # Source: https://www.maxmind.com/en/worldcities
    extract_location_data(location_data_dir+'/'+location_data_file + '.zip',
                          location_data_dir)
    print 'DONE\n'
    
    print 'Loading location data...'
    load_location_data(location_data_dir+'/'+location_data_file,regions)
    print 'DONE\n'
    
    print 'Loading country codes...'
    load_country_codes(location_data_dir+'/'+country_codes_file,country_codes,countries)
    print 'DONE\n'
    
    for file in input_files:
        for yeari in yearsi:
            data = []
            year = str(yeari)
            input_file = input_dir + '/' + file + '_' + year + '.xml'
            output_file = output_dir + '/' + file + '_' + year + '.json'
            process_raw_data(input_file,output_file,year,data,app_id,regions,country_codes,countries)
        
            print('Saving Output File: ' + output_file + '\n')
            with open(output_file,'w') as f:
                json.dump(data,f)   

    print 'Cleaning up extracted location data...'
    cleanup_extracted_location_data(location_data_dir,location_data_file)
    print 'DONE\n'

def extract_location_data(input_file,output_dir):
    zf = zipfile.ZipFile(input_file, "r")
    zf.extractall(output_dir)

def load_location_data(input_file,regions):
    with open(input_file, mode='r') as infile:
        reader = csv.reader(infile)
        for row in reader:
            key = row[1].lower()
            value = row[0].lower()
            
            if key in regions:
                v = regions[key]
                if value not in v:
                    regions[key] = v + ',' + value
            else:
                regions[key] = value

def load_country_codes(input_file,country_codes,countries):
    with open(input_file, mode='r') as infile:
        reader = csv.reader(infile)
        for row in reader:
            country_codes[row[0].lower()] = row[1]
            countries[row[1].lower()] = row[0]

def process_raw_data(input_file,output_file,year,data,app_id,
                     regions,country_codes,countries):
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
        
            country = get_country(affiliations,regions,country_codes,countries)
            
            dict = {'title':title,
                    'authors':authors,
                    'affiliations':affiliations,
                    'doi':doi,
                    'issn':issn,
                    'pdf':pdf,
                    'tags':tags,
                    'citations':citations,
                    'country':country,
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
    
    header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
              'Accept-Encoding': 'none',
              'Accept-Language': 'en-US,en;q=0.8',
              'Connection': 'keep-alive'}

    try:
        request = urllib2.Request(url_title,None,header)
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

def get_country(affiliations,regions,country_codes,countries):
    affiliations = affiliations.strip()
    if len(affiliations) == 0:
        return 'NA'
    
    a_list = affiliations.split(',')
    a_list = [s.strip() for s in a_list]
    
    s = ' '.join(a_list)
    b_list = s.split(' ')
    
    country = extract_country(a_list,regions,country_codes,countries)
    if len(country) > 0:
        return country
    
    return extract_country(b_list,regions,country_codes,countries)
    

def extract_country(list,regions,country_codes,countries):
    if 'USA' in list:
        return country_codes['us']
    
    if 'UK' in list:
        return country_codes['uk']
    
    for s in list:
        s_l = s.lower()
        if s_l in countries:
            return s
        
        if s_l in regions:
            c = regions[s_l]
            if c == 'gb':
                c = 'uk'
            
            if c in country_codes:
                return country_codes[c]
    
    return ''

def cleanup_extracted_location_data(location_data_dir,location_data_file):
    shutil.rmtree(location_data_dir + '/__MACOSX')
    remove(location_data_dir + '/' + location_data_file)
    
if __name__ == "__main__":
    main()