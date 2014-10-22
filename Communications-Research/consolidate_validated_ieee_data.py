import json
import csv
from os import remove

def main():
    # main function
    yearsi = range(2002,2013)
    
    codes = ['iswcs','ew','wowmom','wcnc','vtc_spring','vtc_fall','icc',
             'globecom','pimrc','jsac','tvt','twc','letters']
             
    types = ['conference','conference','conference','conference','conference',
             'conference','conference','conference','conference','journal',
             'journal','journal','journal']
    
    cleanup_data(yearsi)         
    consolidate_ieee_data(yearsi,codes,types)
    consolidate_tags_by_year(yearsi,codes)

def cleanup_data(yearsi):
    try:
        ieee_file = 'final-data/ieee_data.json'
        remove(ieee_file)
    
        for yeari in yearsi:
            year = str(yeari)
            tags_file = 'final-data/tags_' + year + '.csv'
            remove(tags_file)
    except OSError:
        pass

def consolidate_ieee_data(yearsi,codes,types):
    output_data = []
    output_file = 'final-data/ieee_data.json'
    
    print '\n\nConsolidating IEEE Data'
    for index, code in enumerate(codes):
        type = types[index]
        for yeari in yearsi:
            year = str(yeari)
            input_file = 'validated-data/' + code + '_v_' + year + '.json'
            add_data(input_file,code,type,output_data)
        
    print '\nConsolidating data to file: ' + output_file
    with open(output_file,'w') as f:
        json.dump(output_data,f)

def add_data(input_file,code,type,output_data):
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

def consolidate_tags_by_year(yearsi,codes):
    print '\n\nConsolidating Tags Data'
    for yeari in yearsi:
        year = str(yeari)
        output_file = 'final-data/tags_' + year + '.csv'
        for code in codes:
            input_file = 'validated-data/' + code + '_v_' + year + '.json'
            add_tags(input_file,output_file)

def add_tags(input_file,output_file):
    data = json.loads(open(input_file).read())
    
    print '\nProcessing data from file: ' + input_file
    with open(output_file,'ab') as csvfile:
        writer = csv.writer(csvfile,delimiter=',')
        for paper in data:
            authors = paper['authors']
            tags = paper['tags']
            citations = paper['citations']
        
            if len(authors) == 0 or len(tags) == 0:
                continue
        
            tags = tags.split(',')
            for tag in tags:
                tag = tag.lower()
                writer.writerow([tag,citations])
        
if __name__ == "__main__":
    main()