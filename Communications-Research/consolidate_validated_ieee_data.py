import json

def main():
    # main function
    yearsi = range(2002,2013)
    
    codes = ['iswcs','ew','wowmom','wcnc','vtc_spring','vtc_fall','icc',
             'globecom','pimrc','jsac','tvt','twc','letters']
             
    types = ['conference','conference','conference','conference','conference',
             'conference','conference','conference','conference','journal',
             'journal','journal','journal']
             
    consolidate_ieee_data(yearsi,codes,types)

def consolidate_ieee_data(yearsi,codes,types):
    output_data = []
    output_file = 'final-data/ieee_data.json'
    
    for index, code in enumerate(codes):
        type = types[index]
        for yeari in yearsi:
            year = str(yeari)
            input_file = 'validated-data/' + code + '_v_' + year + '.json'
            consolidate_data(input_file,code,type,output_data)
        
    print '\nConsolidating data to file: ' + output_file
    with open(output_file,'w') as f:
        json.dump(output_data,f)

def consolidate_data(input_file,code,type,output_data):
    data = json.loads(open(input_file).read())
    
    print '\nProcessing data from file: ' + input_file
    for paper in data:
        paper['code'] = code
        paper['type'] = type
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