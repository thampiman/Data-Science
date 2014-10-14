import json
import os 
import csv

def main():
    # main function
    yearsi = range(2002,2013)
    
    input_files = ['iswcs','ew','wowmom','wcnc','vtc_spring','vtc_fall','icc',
                   'globecom','pimrc','jsac','tvt','twc','letters']
    
    location_data_dir = 'location-data'
    country_codes_file = 'country_codes.csv'

    country_codes = {}
    countries = {}
    
    print 'Loading country codes...'
    load_country_codes(location_data_dir+'/'+country_codes_file,country_codes)
    print 'DONE\n'
    
    for file in input_files:
        for yeari in yearsi:
            year = str(yeari)
            input_file = 'processed-data/' + file + '_' + year + '.json'
            output_file = 'processed-data/' + file + '_c_' + year + '.json'
            
            print '\nCleaning up file: ' + input_file
            cleanup_data(input_file,output_file,country_codes,countries)

def load_country_codes(input_file,country_codes):
    with open(input_file, mode='r') as infile:
        reader = csv.reader(infile)
        for row in reader:
            country_codes[row[0].lower()] = row[1]

def cleanup_data(input_file,output_file,country_codes,countries):
    data = json.loads(open(input_file).read())
    
    # for paper in data:
    for index, paper in enumerate(data):
        title = paper['title']
        doi = paper['doi']
        year = paper['year']
        citations = paper['citations']
        affiliations = paper['affiliations']
        
        a_list = affiliations.split(',')
        a_list = [s.strip() for s in a_list]
        
        if citations < 0:
            print '\nTitle: ' + title
            print 'DOI: ' + doi
            print 'Year: ' + year
            
            # Makes data entry a lot easier by copying GS link to clipboard
            # (works only on the Mac)
            query = 'http://scholar.google.co.uk/scholar?q='
            if len(doi) != 0:
                query = query + doi
            else:
                query = query + title
            query = query + '&btnG=&hl=en&as_sdt=0%2C5'
            os.system("echo '%s' | pbcopy" % query)
            
            citation_i = 0
            while True:
                citation_s = raw_input('Enter citations for paper: ')
                if integer(citation_s):
                    citation_i = int(citation_s)
                    if citation_i == 0:
                        citation_i = -2
                    break
            
            paper['citations'] = citation_i
            
        country = paper['country']
        
        if len(country) == 0:
            print '\nTitle: ' + title
            print 'Affiliations: ' + affiliations
            print 'Year: ' + year
            
            for s in a_list:
                if s in countries:
                    country = countries[s]
                    print 'Country set to: ' + country
                    paper['country'] = country
                    break
            
            if len(country) == 0:
                while True:
                    code = raw_input('Enter 2-letter country code: ')
                    if code in country_codes:
                        country = country_codes[code]
                        paper['country'] = country
                        for s in a_list:
                            countries[s] = country
                        break
    
    with open(output_file,'w') as f:
        json.dump(data,f)

def integer(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    main()