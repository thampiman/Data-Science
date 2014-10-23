import json
import csv
from os import remove

def main():
    # main function
    years = [str(year) for year in range(2002,2013)]
    
    codes = ['iswcs','ew','wowmom','wcnc','vtc_spring','vtc_fall','icc',
             'globecom','pimrc','jsac','tvt','twc','letters']
             
    types = ['conference','conference','conference','conference','conference',
             'conference','conference','conference','conference','journal',
             'journal','journal','journal']
    
    cleanup_data(years)         
    consolidate_ieee_data(years,codes,types)
    consolidate_tags_by_year(years,codes)

def cleanup_data(years):
    try:
        ieee_file = 'final-data/ieee_data.json'
        remove(ieee_file)
    
        for year in years:
            tags_file = 'final-data/tags_' + year + '.csv'
            remove(tags_file)
    except OSError:
        pass

def consolidate_ieee_data(years,codes,types):
    output_data = []
    output_file = 'final-data/ieee_data.json'
    
    print '\n\nConsolidating IEEE Data'
    for index, code in enumerate(codes):
        type = types[index]
        for year in years:
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

def consolidate_tags_by_year(years,codes):
    print '\n\nConsolidating Tags Data'
    for year in years:
        output_file = 'final-data/tags_' + year + '.json'
        tags_dict = {}
        for code in codes:
            input_file = 'validated-data/' + code + '_v_' + year + '.json'
            add_tags(input_file,tags_dict)

        output_data = []
        print '\nFormatting Tags Dictionary for ' + year
        for key,value in tags_dict.iteritems():
            d = {}
            d['tag'] = key
            d['pubs'] = value['pubs']
            d['citations'] = value['citations']
            d['citations_per_pub'] = d['citations'] / float(d['pubs'])
            titles = str(value['titles'])
            titles = titles.replace(',',';')
            d['titles'] = titles
            output_data.append(d)
        
        print '\nConsolidating data to file: ' + output_file
        with open(output_file,'w') as f:
            json.dump(output_data,f)

def add_tags(input_file,tags_dict):
    data = json.loads(open(input_file).read())
    
    print '\nProcessing data from file: ' + input_file
    for paper in data:
        title = paper['title']
        authors = paper['authors']
        tags = paper['tags']
        citations = paper['citations']
    
        if len(authors) == 0 or len(tags) == 0:
            continue
    
        tags = tags.split(',')
        for tag in tags:
            tag = tag.lower()
            if tag in tags_dict:
                tag_data = tags_dict[tag]
                tag_data['pubs'] += 1
                tag_data['citations'] += citations
                tag_data['titles'].append(title)
            else:
                tag_data = {}
                tag_data['pubs'] = 1
                tag_data['citations'] = citations
                tag_data['titles'] = [title]
                tags_dict[tag] = tag_data
        
if __name__ == "__main__":
    main()