# All constant objects consolidated in one file

from shapely.geometry import Point
from enum import Enum

airport_coordinates = [
    {'location': [51.4700, -0.4543]},
    {'location': [51.1537, -0.1821]},
    {'location': [51.8763, -0.3717]},
    {'location': [51.5048, 0.0495]},
    {'location': [51.8860, 0.2389]}
]

airport_points = [ 
    Point(
        list(x.values())[0][1],
        list(x.values())[0][0]
    ) 
    for x 
    in airport_coordinates
    ]

discrete_continuous_map = {
    '<=54.9' : 0,
    '55.0-59.9' : 550,
    '60.0-64.9' : 600,
    '65.0-69.9' : 650,
    '70.0-74.9' : 700,
    '>=75.0' : 750
}

daytime_noise_useful_keys = [
    "pedal_cycles",
    "cars_and_taxis",
    "buses_and_coaches",
    "lgvs",
    "road_noise_day"
]
nighttime_noise_useful_keys = [
    "pedal_cycles",
    "cars_and_taxis",
    "buses_and_coaches",
    "lgvs",
    "all_hgvs",
    "people_at_closest_tube_station",
    "distance_to_london",
    "road_noise_night"
]
light_useful_keys = [
    "pedal_cycles",
    "two_wheeled_motor_vehicles",
    "cars_and_taxis",
    "buses_and_coaches",
    "lgvs",
    "population",
    "distance_to_closest_tube_station",
    "people_at_closest_tube_station",
    "distance_to_closest_airport",
    "distance_to_london",
    'light_pollution'
]
daytime_noise_outlier_keys = [
    'buses_and_coaches',
    'cars_and_taxis',
]
nighttime_noise_outlier_keys = [
    'buses_and_coaches',
    'cars_and_taxis',
    'people_at_closest_tube_station'
]
light_outlier_keys = [
    'buses_and_coaches',
    'cars_and_taxis',
    'distance_to_closest_tube_station',
    'people_at_closest_tube_station',
    'two_wheeled_motor_vehicles'
]

class Pollution:
    def __init__(self, useful_keys, outlier_keys, type_of_pollution, filepath):
        self.useful_keys = useful_keys
        self.outlier_keys = outlier_keys
        self.type_of_pollution = type_of_pollution
        self.filepath = filepath

class PollutionTypes(Enum):
    daytime_noise = Pollution(daytime_noise_useful_keys, daytime_noise_outlier_keys,'road_noise_day', 'data/traffic/traffic_data_with_noise_and_population_and_proximity.geojson')
    nighttime_noise = Pollution(nighttime_noise_useful_keys, nighttime_noise_outlier_keys,'road_noise_night', 'data/traffic/traffic_data_with_noise_and_population_and_proximity.geojson')
    light = Pollution(light_useful_keys, light_outlier_keys,'light_pollution', 'data/traffic/full_traffic_data.geojson')

def getPollutionObject(pollution_type):
    if pollution_type == "light":
        return PollutionTypes.light.value
    elif pollution_type == "noise day":
        return PollutionTypes.daytime_noise.value
    elif pollution_type == "noise night":
        return PollutionTypes.nighttime_noise.value
    raise Exception('Invalid pollution type specified')