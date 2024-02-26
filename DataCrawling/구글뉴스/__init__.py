
import os
import sys
sys.path.append('/Users/genie/Documents/COLLABORATION/Tokyo-Airbnb-Project/DataCrawling')
sys.path.append('/Users/genie/Documents/COLLABORATION/Tokyo-Airbnb-Project/DataCrawling/OshimaLand')

import pandas as pd

import OshimaLand.tokyo_metro as ot

if __name__ == "__main__":
    base_path = '/Users/genie/Documents/COLLABORATION/Tokyo-Airbnb-Project/DataCrawling' 
    file_name = os.path.join(base_path, 'Oshimaland/line_detail_kr.pkl')
    df = pd.read_pickle(file_name)
    print(df)