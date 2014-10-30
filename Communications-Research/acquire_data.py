import urllib2

def main():
    years = [str(year) for year in range(2002,2013)]
    journals = [('ISWCS','iswcs'),
                ('European%20Wireless%20Conference','ew'),
                ('IEEE%20WoWMoM','wowmom'),
                ('WCNC','wcnc'),
                ('VTC%20Spring','vtc_spring'),
                ('VTC%20Fall','vtc_fall'),
                ('ICC','icc'),
                ('Globecom','globecom'),
                ('PIMRC','pimrc'),
                ('Selected%20Areas%20in%20Communications','jsac'),
                ('Transactions%20on%20Vehicular%20Technology','tvt'),
                ('Transactions%20on%20Wireless%20Communications','twc'),
                ('Communications%20Letters','letters')]
    
    for (journal,filename) in journals:
        for year in years:
            output_file = 'raw-data/' + filename + '_' + year + '.xml'
            fetch_data(year,journal,output_file)

def fetch_data(year,journal,output_file):
    url = 'http://ieeexplore.ieee.org/gateway/ipsSearch.jsp?py=' + year + '&jn=' + journal + '&hc=1000'
    
    print 'Fetching Journal = ' + journal + ' for Year = ' + year
    response = urllib2.urlopen(url)
    
    print 'Saving Raw Data to ' + output_file + '\n'
    xml = response.read()
    f = open(output_file,'w')
    f.write(xml)
    f.close()

if __name__ == "__main__":
    main()