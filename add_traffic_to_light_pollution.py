# Script to add light pollution data to traffic file
# Input: Traffic data for 2015 and light pollution data
# Output: Light pollution-enriched traffic data

import json
from shapely.geometry import Polygon, shape, mapping, Point

london_traffic_2015 = json.load(
    open('data/traffic/london_traffic_2015.geojson'))
light_pollution_data = json.load(
    open('data/london_light_pollution_2015.geojson'))

light_pollution_objects = light_pollution_data['features']

# Find out each traffic point's light pollution level
for traffic_obj in london_traffic_2015['features']:
    traffic_point = Point(traffic_obj['geometry']['coordinates'])

    for light_pollution_object in light_pollution_objects:
        light_pollution_multipolygon = shape(
            light_pollution_object['geometry'])

        # Enrich traffic data point with light pollution level
        for light_pollution_polygon in light_pollution_multipolygon:
            if light_pollution_polygon.contains(traffic_point):
                light_pollution_level = light_pollution_object['properties']['DN']
                traffic_obj['properties']['light_pollution'] = light_pollution_level
                break

output = open('data/light/light_pollution_with_traffic.geojson', 'w')
json.dump(london_traffic_2015, output)
