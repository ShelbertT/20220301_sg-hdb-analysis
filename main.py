# Nomenclature for this project generally follows PEP8 rules, with some customized exceptions
#   Class Names: PascalCase (similar to CamelCase)
#   Global Variables Names: CamelCase
#   Function Names: UnderScoreCase, and starts with a verb
#       Argument names: All lower case
#       Local Variables Names: UnderScoreCase

import copy
from visualization import *
from rawProcessing import *
from getConvexHull import *
from geoAnalysis import *
import math
import getpass


def assign_value(origin, convex_hull):
    origin_copy = copy.deepcopy(origin)
    convex_hull_copy = copy.deepcopy(convex_hull)

    convert_coordinate(origin_copy)
    convert_coordinate(convex_hull_copy)

    # First, calculate the essential value for each building based on original data.
    height_name = "HDB_cleaning.height"
    carbon_name = "hdb_carbon.csv.hdb_total_carbon"

    for feature in origin_copy['features']:
        polygons = feature['geometry']['coordinates']
        building_num = len(polygons)
        total_surface_area = 0
        total_shape_area = 0
        total_height = building_num * feature['properties'][height_name]

        for polygon in polygons:
            total_surface_area += get_surface_area(polygon, feature['properties'][height_name])
            total_shape_area += get_shape_area(polygon)

        total_carbon_efficiency = feature['properties'][carbon_name] / total_surface_area

        # Add new properties to the geojson
        feature['properties']['total_shape_area'] = total_shape_area
        feature['properties']['total_carbon_efficiency'] = total_carbon_efficiency
        feature['properties']['total_height'] = total_height
        feature['properties']['building_num'] = building_num

    # Second, calculate the area of each convex_hull_copy and assign them back to origin convex_hull
    for i in range(len(convex_hull['features'])):
        convex_hull_area = get_shape_area(convex_hull_copy['features'][i]['geometry']['coordinates'][0])

        properties = convex_hull['features'][i]['properties']
        properties['convex_hull_area'] = convex_hull_area
        # Also initialize some wanted properties in advance
        properties['building_area'] = 0
        properties['carbon_efficiency'] = 0  # temp
        properties['total_height'] = 0  # temp
        properties['building_number'] = 0

    # Second (pt2), get all precinct names
    all_precincts = []
    for feature in convex_hull["features"]:
        precinct_name = feature["properties"]["hdb_street"]
        if precinct_name not in all_precincts:
            all_precincts.append(precinct_name)

    # Third, Summarize the wanted information into convex_hull
    for feature in convex_hull['features']:
        properties = feature['properties']
        precinct_name = properties['hdb_street']
        for feature1 in origin_copy['features']:
            properties1 = feature1['properties']
            if properties1['HDB_cleaning.hdb_street'] == precinct_name:
                properties['building_area'] += properties1['total_shape_area']
                properties['carbon_efficiency'] += properties1['total_carbon_efficiency']  # temp
                properties['total_height'] += properties1['total_height']  # temp
                properties['building_number'] += properties1['building_num']
            else:
                continue

    # Fourth, calculate the average value based on convex_hull
    for feature in convex_hull['features']:
        properties = feature['properties']
        properties['density'] = properties['building_area'] / properties['convex_hull_area']
        properties['carbon_efficiency'] = properties['carbon_efficiency'] / properties['building_number']
        properties['average_height'] = properties['total_height'] / properties['building_number']

        properties.pop('convex_hull_area')
        properties.pop('building_area')
        properties.pop('total_height')
        properties.pop('building_number')

    return convex_hull


def main(threshold=450000):
    original_data = read_json(origin)

    # Using deepcopy Because the following function will modify the original data, and wee need the original data later.
    convex_hull = generate_convex_hull_geojson(copy.deepcopy(original_data), threshold)
    write_json(convex_hull, convex)

    return assign_value(original_data, convex_hull)


if __name__ == '__main__':
    origin = 'data/hdb_carbon.geojson'
    convex = 'output/convex_hull.geojson'

    username = getpass.getuser()

    passcode = False
    print(f'Welcome, {username}. How\'s your day?')
    print('-------------------------------------------')
    print('[Actions Supported] \n'
          'generate: threshold is needed \n'
          'showmap: geojson is needed \n'
          'exit: exit the program\n')

    while not passcode:
        command = input('Input Command: ')
        command = command.split()  # 在这里command变成了列表
        if len(command) == 1:
            act = command[0]
            param = None
        elif len(command) == 2:
            act = command[0]
            try:
                param = int(command[1])
            except:
                param = command[1]
        else:
            print('[Warning] Wrong input format\n')
            continue

        if act == 'generate':
            main(param)
            print(f'[DONE] A convex hull using {param} as threshold is generated. You can find it here: {convex}.')
        elif act == 'showmap':
            if param == 'origin':
                map_shown = read_json(origin)
                print('[DONE] Original data is shown.')
            elif param == 'convex':
                map_shown = read_json(convex)
                print('[DONE] Convex hull is shown.')
            show_map(map_shown)
        elif act == 'exit':
            passcode = True
        else:
            print('[Warning] Wrong input format\n')
            continue
        print('\n')
