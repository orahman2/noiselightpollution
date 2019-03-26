import json
from shapely.geometry import shape, Point
# depending on your version, use: from shapely.geometry import shape, Point

# load GeoJSON file containing sectors
with open('light_pixels.geojson') as f:
    js = json.load(f)

print('loaded light pollution file congrats.')

# construct point based on lon/lat returned by geocoder
point = Point(51.5074, -0.1278)

# check each polygon to see if it contains the point
for feature in js['features']:
    polygon = shape(feature['geometry'])
    if polygon.contains(point):
        print('Found containing polygon:', feature)