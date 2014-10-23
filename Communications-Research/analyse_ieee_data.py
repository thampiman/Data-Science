from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import pandasql

def main():
    years = [str(year) for year in range(2002,2013)]
    
    # Load IEEE data
    ieee_data = load_ieee_data()
    
    # Load Tags data
    tags_data = load_tags_data(years)
    
    # Analyse the IEEE data
    analyse_countries(ieee_data)
    analyse_publications(ieee_data)
    
    # Analyse the Tags Data
    analyse_tags(tags_data,years)
    
def load_ieee_data():
    ieee_data = pd.read_json('final-data/ieee_data.json')
    
    # Format Country and Tags strings
    country_format = lambda x: np.NaN if x == 'NA' else x.lower()
    tags_format = lambda x: np.NaN if x == '' else x.lower()
    ieee_data['country'] = ieee_data['country'].map(country_format)
    ieee_data['tags'] = ieee_data['tags'].map(tags_format)
    
    return ieee_data

def load_tags_data(years):
    tags_data = {}
    for year in years:
        tags_file = 'final-data/tags_' + year + '.json'
        tags_df = pd.read_json(tags_file)
        tags_data[year] = tags_df
        
    return tags_data

def analyse_countries(ieee_data):
    grouped = ieee_data.groupby('country')
    grouped_citations = grouped['citations']
    
    pubs = grouped_citations.count()
    citations = grouped_citations.sum()
    
    pubs_filtered = pubs[pubs >= 100]
    citations_filtered = citations[pubs >= 100]
    citations_per_pub = citations_filtered / pubs_filtered
    
    pubs.sort(ascending=False)
    citations_filtered.sort(ascending=False)
    citations_per_pub.sort(ascending=False)
        
    print 'Number of Publications by Country'
    print '---------------------------------'
    print pubs[0:20]
    print '\n'
    print 'Number of Citations by Country'
    print '------------------------------'
    print citations_filtered[0:20]
    print '\n'
    print 'Number of Citations per Publication by Country'
    print '----------------------------------------------'
    print citations_per_pub[0:20]
    print '\n'

    pubs.to_csv('analysed-data/pubs_by_country.csv')
    citations_filtered.to_csv('analysed-data/citations_by_country.csv')
    citations_per_pub.to_csv('analysed-data/citations_per_pub_by_country.csv')

def analyse_publications(ieee_data):
    pubs = ieee_data.groupby(['code','year'])['citations'].count().unstack()
    citations = ieee_data.groupby(['code','year'])['citations'].sum().unstack()
    citations_per_pub = citations / pubs

    print 'Number of Publications by Code and Year'
    print '---------------------------------------'
    print pubs
    print '\n'
    print 'Number of Citations by Code and Year'
    print '------------------------------------'
    print citations
    print '\n'
    print 'Number of Citations per Publication by Code and Year'
    print '----------------------------------------------------'
    print citations_per_pub
    print '\n'

    pubs.to_csv('analysed-data/pubs_by_year_code.csv')
    citations.to_csv('analysed-data/citations_by_year_code.csv')
    citations_per_pub.to_csv('analysed-data/citations_per_pub_by_year_code.csv')

def analyse_tags(tags_data,years):
    for year in years:
        tags_df = tags_data[year]
        
        pubs = tags_df.sort(columns='pubs',ascending=False,inplace=False)
        citations = tags_df.sort(columns='citations',ascending=False,inplace=False)
        citations_per_pub = tags_df.sort(columns='citations_per_pub',ascending=False,inplace=False)
                
        print 'Top 20 Tags by Publications for ' + year 
        print '------------------------------------'
        print pubs[0:20]
        print '\n'
        print 'Top 20 Tags by Citations for ' + year
        print '---------------------------------'
        print citations[0:20]
        print '\n'
        print 'Top 20 Tags by Citations per Publication for ' + year
        print '-------------------------------------------------'
        print citations_per_pub[0:20]
        print '\n'
        
        pubs.to_csv('analysed-data/pubs_by_tags_' + year + '.csv')
        citations.to_csv('analysed-data/citations_by_tags_' + year + '.csv')
        citations_per_pub.to_csv('analysed-data/citations_per_pub_by_tags_' + year + '.csv')

if __name__ == "__main__":
    main()