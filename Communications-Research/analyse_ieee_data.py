from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import pandasql

def main():
    # Load IEEE data
    ieee_data = load_ieee_data()
    
    # Analyse the IEEE data
    # analyse_tags(ieee_data)
    analyse_countries(ieee_data)
    # analyse_publications(ieee_data)
    
def load_ieee_data():
    ieee_data = pd.read_json('final-data/ieee_data.json')
    
    # Format Country and Tags strings
    country_format = lambda x: np.NaN if x == 'NA' else x.lower()
    tags_format = lambda x: np.NaN if x == '' else x.lower()
    ieee_data['country'] = ieee_data['country'].map(country_format)
    ieee_data['tags'] = ieee_data['tags'].map(tags_format)
    
    return ieee_data

def analyse_tags(ieee_data):
    grouped = ieee_data.groupby(['year','tags'])
    data_by_year = grouped.sum()

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
    pubs_by_yr_code = ieee_data.groupby(['code','year'])['citations'].count().unstack()
    citations_by_yr_code = ieee_data.groupby(['code','year'])['citations'].sum().unstack()
    quality_by_yr_code = citations_by_yr_code / pubs_by_yr_code

    print 'Number of Publications grouped by Code and Year'
    print '-----------------------------------------------'
    print pubs_by_yr_code
    print '\n'
    print 'Quality of Publications grouped by Code and Year'
    print '------------------------------------------------'
    print quality_by_yr_code
    print '\n'

    #pubs_by_yr_code.to_csv('analysed-data/publications_by_year_code.csv')
    #quality_by_yr_code.to_csv('analysed-data/quality_of_publications_by_year_code.csv')

if __name__ == "__main__":
    main()