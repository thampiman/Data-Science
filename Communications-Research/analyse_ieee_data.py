from pandas import Series, DataFrame
import pandas as pd
import numpy as np

def main():
    # Conferences
    ew = pd.read_json('final-data/ew.json')
    globecom = pd.read_json('final-data/globecom.json')
    icc = pd.read_json('final-data/icc.json')
    iswcs = pd.read_json('final-data/iswcs.json')
    pimrc = pd.read_json('final-data/pimrc.json')
    vtc_fall = pd.read_json('final-data/vtc_fall.json')
    vtc_spring = pd.read_json('final-data/vtc_spring.json')
    wcnc = pd.read_json('final-data/wcnc.json')
    wowmom = pd.read_json('final-data/wowmom.json')
    
    # Journals
    jsac = pd.read_json('final-data/jsac.json')
    letters = pd.read_json('final-data/letters.json')
    tvt = pd.read_json('final-data/tvt.json')
    twc = pd.read_json('final-data/twc.json')

if __name__ == "__main__":
    main()