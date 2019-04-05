# All constant objects consolidated in one file

from shapely.geometry import Point

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