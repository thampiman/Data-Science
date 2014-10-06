import json

def main():
    # main function
    yearsi = range(2002,2013)
    
    #input_files = ['iswcs','ew','wowmom','wcnc','vtc_spring','vtc_fall','icc',
    #               'globecom','pimrc','jsac','tvt','twc','letters']
    input_files = ['wowmom']
    
    for file in input_files:
        for yeari in yearsi:
            year = str(yeari)
            input_file = 'processed-data/' + file + '_c_' + year + '.json'
            output_file = 'processed-data/' + file + '_v_' + year + '.json'
            
            validate_data(input_file,output_file)

def validate_data(input_file,output_file):
    data = json.loads(open(input_file).read())
    
    for paper in data:
        title = paper['title']
        doi = paper['doi']
        year = paper['year']
        citations = paper['citations']
        
        if citations == 0 or citations > 40:
            print '\nTitle: ' + title
            print 'DOI: ' + doi
            print 'Year: ' + year
            
            citation_i = 0
            while True:
                citation_s = raw_input('Enter citations for paper: ')
                if citation_s.isdigit():
                    citation_i = int(citation_s)
                    break
            
            paper['citations'] = citation_i
        elif citations == -2:
            paper['citations'] = 0
    
    with open(output_file,'w') as f:
        json.dump(data,f)

if __name__ == "__main__":
    main()