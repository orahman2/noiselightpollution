# Script to produce files that predict noise and light pollution for different years
# Input: London road traffic data, tube coordinates, population data
# Output: Pollution data segregated by year

import json
import util
import shapely
from shapely.geometry import Point, shape, GeometryCollection
import constants
import util

tube_station_data = json.load(open("data/london_tube_coordinates.json"))
population_data = json.load(open("data/population/london_post_code_sector_population.geojson"))

# Build list of polygons enriched with population
def build_polygon_population_list():
    polygon_list = util.get_polygon_list(population_data)
    return [
        [
            polygon_list[polygon_list_index],
            population_data['features'][polygon_list_index]["properties"]['population']
        ]
        for polygon_list_index in range(0, len(polygon_list))
    ]

population_list = build_polygon_population_list()

# Enrich traffic points for each year
for year_suffix in range(0, 18):

    # Load correct traffic file
    year = f"200{year_suffix}" if year_suffix < 10 else f"20{year_suffix}"
    london_traffic = json.load(open(f"data/traffic/london_traffic_{year}.geojson"))

    # For each traffic point, generate various distance based properties
    for feature in london_traffic['features']:
        closest_tube_station = sorted(
            tube_station_data,
            key=lambda tube_obj: util.get_distance_to_place(feature, tube_obj)
        )[0]
        
        distance_to_closest_tube = util.get_distance_to_place(feature, closest_tube_station)
        distance_to_central_london = util.get_distance_to_place(feature, {'location':[51.5074, -0.1278]})

        closest_airport = sorted(
            constants.airport_coordinates,
            key=lambda airport_obj: util.get_distance_to_place(feature, airport_obj)
        )[0]

        # Add population to each traffic point
        for population_obj in population_list:
            population_polygon = population_obj[0]
            population = population_obj[1]

            if population_polygon.contains(Point(feature['geometry']['coordinates'])):
                feature['properties']['population'] = population

        if 'population' not in feature['properties']:
            continue

        feature['properties']['distance_to_central_london'] = distance_to_central_london
        feature['properties']['distance_to_closest_tube_station'] = distance_to_closest_tube
        feature['properties']['people_at_closest_tube_station'] = closest_tube_station['people_count']
        feature['properties']['distance_to_closest_airport'] = util.get_distance_to_place(feature, closest_airport)

        # Apply formulae obtained by performing multivariate regression
        feature['properties']['noise_pollution_day'] = (64.3830 +
            0.0004*feature['properties']['cars_and_taxis'] + 
            0.0009*feature['properties']['pedal_cycles'] + 
            0.0034*feature['properties']['buses_and_coaches'] +
            0.0010*feature['properties']['lgvs']
        )

        feature['properties']['noise_pollution_night'] = (62.8828 +
            0.0010*feature['properties']['pedal_cycles'] +
            0.0003*feature['properties']['cars_and_taxis'] + 
            0.0032*feature['properties']['buses_and_coaches'] +
            0.0008*feature['properties']['lgvs'] +
            0.0016*feature['properties']['all_hgvs'] +
            4.187e-07*feature['properties']['people_at_closest_tube_station'] +
            0.1508*feature['properties']['distance_to_central_london']
        )

        feature['properties']['light_pollution'] = (81.9627 +
            0.0009*feature['properties']['pedal_cycles'] +
            0.0015*feature['properties']['two_wheeled_motor_vehicles'] +
            8.134e-05*feature['properties']['cars_and_taxis'] + 
            -0.0010*feature['properties']['buses_and_coaches'] +
            -0.0004*feature['properties']['lgvs'] +
            0.0329*feature['properties']['population'] +
            1.2253*feature['properties']['distance_to_closest_tube_station'] +
            -2.109e-07*feature['properties']['people_at_closest_tube_station'] +
            0.0708*feature['properties']['distance_to_closest_airport'] +
            -0.2323*feature['properties']['distance_to_central_london']
        )

    print(f"done with file for year {year}")
    json.dump(london_traffic, open(f"data/final_output/data_points_{year}.geojson", 'w'))