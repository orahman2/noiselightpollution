# Script to consume department of transport's REST API
# Input: REST API url
# Output: traffic data

import requests
import json
import ssl
import time
from sys import argv

# place type is either local authority or region
script, place_type, place_id = argv

# Download first page, set mandatory variables
ssl.OPENSSL_VERSION
url = f"https://roadtraffic.dft.gov.uk/api/average-annual-daily-flow?filter[{place_type}_id]={place_id}"
filename = f"data/traffic/traffic_data_{place_type}_{place_id}.json"
r_lon_main_req = requests.get(url)
r_lon_main = r_lon_main_req.json()
num_pages = r_lon_main['meta']['last_page']
page = 2

# Check if script was run previously and quit halfway
# If so, continue from where it left off
try:
    previous_file = json.load(open(filename))
    timed_out_on_page = previous_file['time_out_page']
    if timed_out_on_page is not None:
        page = int(timed_out_on_page)
    r_lon_main = previous_file
except:
    print('attempting for first time')

for page in range(page, num_pages + 1):
    page = str(page)
    r_lon_req = requests.get(url+"&page[number]="+page)
    if r_lon_req.status_code is not 200:
        print('timed out')
        r_lon_main['time_out_page'] = page
        break
    r_lon = r_lon_req.json()
    r_lon_main['data'].extend(r_lon['data'])

with open(filename, 'w') as outfile:
    json.dump(r_lon_main, outfile)