import json
import os 
import csv

def main():
    # main function
    location_data_dir = 'location-data'
    country_codes_file = 'country_codes.csv'

    country_codes = {}
    countries = {}
    
    print 'Loading country codes...'
    load_country_codes(location_data_dir+'/'+country_codes_file,country_codes)
    print 'DONE\n'
    
    input_file = 'final-data/ieee_data.json' 
    output_file = 'final-data/ieee_data2.json'
            
    print '\nCleaning up file: ' + input_file
    cleanup_data(input_file,output_file,country_codes,countries)

def load_country_codes(input_file,country_codes):
    with open(input_file, mode='r') as infile:
        reader = csv.reader(infile)
        for row in reader:
            country_codes[row[0].lower()] = row[1]

def cleanup_data(input_file,output_file,country_codes,countries):
    data = json.loads(open(input_file).read())
    
    for paper in data:
        title = paper['title']
        doi = paper['doi']
        year = paper['year']
        citations = paper['citations']
        affiliations = paper['affiliations']
            
        country = paper['country']
        
        a_list = affiliations.split(',')
        a_list = [s.strip() for s in a_list]
        
        if country.lower() == 'australia':
            print '\nTitle: ' + title
            print 'Affiliations: ' + affiliations
            print 'Year: ' + year
            
            country_set = False
            for s in a_list:
                if s in countries:
                    country = countries[s]
                    print 'Country set to: ' + country
                    paper['country'] = country
                    country_set = True
                    break
            
            if not country_set:
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