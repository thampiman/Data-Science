import json

def main():
    # main function
    yearsi = range(2002,2013)
    
    input_files = ['iswcs','ew','wowmom','wcnc','vtc_spring','vtc_fall','icc',
                   'globecom','pimrc','jsac','tvt','twc','letters']
    
    for file in input_files:
        output_data = []
        output_file = 'final-data/' + file + '.json'
        for yeari in yearsi:
            year = str(yeari)
            input_file = 'processed-data/' + file + '_v_' + year + '.json'
            consolidate_data(input_file,output_file,output_data)
        
        print '\nConsolidating data to file: ' + output_file
        with open(output_file,'w') as f:
            json.dump(output_data,f)

def consolidate_data(input_file,output_file,output_data):
    data = json.loads(open(input_file).read())
    
    print '\nProcessing data from file: ' + input_file
    for paper in data:
        title = paper['title']
        authors = paper['authors']
        tags = paper['tags']
        
        # final cleanup
        if len(authors) == 0 or len(tags) == 0:
            print 'Removing paper: ' + title
            continue
        
        output_data.append(paper)

if __name__ == "__main__":
    main()