import json
import util

tube_station_data = json.load(open("london_tube_coordinates.json"))

def get_distance_to_place(traffic_feature, place):
    y1 = traffic_feature['geometry']['coordinates'][0]
    x1 = traffic_feature['geometry']['coordinates'][1]
    x2 = place['location'][0]
    y2 = place['location'][1]
    return util.distance(x1, y1, x2, y2)

for year_suffix in range(0, 18):
    year = f"200{year_suffix}" if year_suffix < 10 else f"20{year_suffix}"
    london_traffic = json.load(open(f"london_traffic_{year}.geojson"))
    for feature in london_traffic['features']:
        closest_tube_station = sorted(tube_station_data, key=lambda tube_obj: get_distance_to_place(feature, tube_obj))[0]
        distance_to_closest_tube = get_distance_to_place(feature, closest_tube_station)
        feature['properties']['distance_to_closest_tube_station'] = distance_to_closest_tube

        feature['properties']['noise_pollution_day'] = (66.4126 +
        0.0002*feature['properties']['cars_and_taxis'] + 
        0.0017*feature['properties']['two_wheeled_motor_vehicles'] + 
        0.0034*feature['properties']['buses_and_coaches'] +
        0.0011*feature['properties']['lgvs'])

        feature['properties']['noise_pollution_night'] = (66.1631 +
        0.0002*feature['properties']['cars_and_taxis'] + 
        0.0034*feature['properties']['buses_and_coaches'] +
        0.0016*feature['properties']['lgvs'])

        feature['properties']['light_pollution'] = (83.6482 +
        -0.0001*feature['properties']['cars_and_taxis'] + 
        -0.0004*feature['properties']['all_hgvs'] + 
        0.0007*feature['properties']['lgvs'] + 
        0.0017*feature['properties']['buses_and_coaches'] +
        0.2430*feature['properties']['distance_to_closest_tube_station'])

    print(f"done with file for year {year}")

    json.dump(london_traffic, open(f"data_points_{year}.geojson", 'w'))