import os
import itertools
import sys

sys.path.append(
    "/Users/genie/Documents/COLLABORATION/Tokyo-Airbnb-Project/DataCrawling"
)
sys.path.append(
    "/Users/genie/Documents/COLLABORATION/Tokyo-Airbnb-Project/DataCrawling/OshimaLand"
)
sys.path.append(
    "/Users/genie/Documents/COLLABORATION/Tokyo-Airbnb-Project/DataCrawling/Googlenews"
)

import Googlenews.googlenews as gn

if __name__ == "__main__":
    base_path = "/Users/genie/Documents/COLLABORATION/Tokyo-Airbnb-Project/DataCrawling"
    file_name = os.path.join(base_path, "Oshimaland/line_detail_kr.pkl")
    result = gn.open_dict(file_name)
    station_tmp = []
    for idx, (key, value) in enumerate(result.items()):
        station_tmp.append(value)
    station_list = list(itertools.chain(*station_tmp))

    station_list_korean = [
        gn.pattern_regex(station)
        for station in station_list
        if gn.pattern_regex(station)
    ]
 
