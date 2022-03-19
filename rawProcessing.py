from visualization import *
import json
import copy


# Creating Geojson-------------------------------------------------------------------------------------------------------
class GeoJSON:  # Access through self.geojson
    def __init__(self, name):
        self.name = name

        self.geojson = {
            "name": name,
            "crs": {
                "type": "name",
                "properties": {
                    "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
                }
            },
            "features": [],
            "type": "FeatureCollection"
        }

    def add_feature(self, feature):  # Feature class
        self.geojson["features"].append(feature.feature)

    def get_all_streets(self):  # check all streets stored in the current geojson
        all_streets = []
        if len(self.geojson["features"]) > 0:
            for feature in self.geojson["features"]:
                street_name = feature["properties"]["hdb_street"]
                if street_name not in all_streets:
                    all_streets.append(street_name)

        return all_streets


class Feature:  # Access through self.feature
    def __init__(self, polygons, feature_id, properties={}):
        self.feature_id = feature_id

        self.feature = {
            "geometry": {
                "coordinates": polygons,
                "type": "Polygon"
            },
            "id": feature_id,
            "properties": properties,
            "type": "Feature"
        }

    def add_polygons(self, polygons):  # list[list[x, y]]
        self.feature["geometry"]["coordinates"] += polygons

    def add_property(self, property):  # dict{}
        self.feature["geometry"]["properties"].update(property)

    # def remove_feature(self, feature_name):  # remove the specified feature
    #     self.


class Properties:  # Access through self.all
    def __init__(self, hdb_street):
        self.all = {
            "hdb_street": hdb_street
        }


# JSON------------------------------------------------------------------------------------------------------------------
# path -> dict | 输入文件路径，返回存储该json的字典
def read_json(input_path):
    with open(input_path, encoding='utf-8') as f:
        resp = json.load(f)

    reclassification(resp)
    return resp


# dict -> json | 把字典写入本地json文件
def write_json(data, output_path='test.json'):
    with open(output_path, "w", encoding='utf-8') as f:
        # json.dump(dict_var, f)  # 写为一行
        json.dump(data, f, indent=2, sort_keys=True, ensure_ascii=False)  # 写为多行


# Switch Coordinates------------------------------------------------------------------------------------------------------------------
# Use Haversine formula to calculate great-circle distance in meters
def get_great_circle_distance(lon1, lat1, lon2, lat2):
    p = math.pi/180
    a = 0.5 - math.cos((lat2 - lat1) * p) / 2 + math.cos(lat1 * p) * math.cos(lat2 * p) * (1 - math.cos((lon2 - lon1) * p)) / 2
    return 12742 * math.asin(math.sqrt(a)) * 1000  # 2*R*asin...


# GeoJSON -> GeoJSON | # Calculate a centre point as the origin point of a new coordinate system, then convert the origin coordinates into new one
def convert_coordinate(geojson):
    longitudes = []
    latitudes = []

    # Get the min for lon and lat, then get the origin point
    for feature in geojson['features']:
        polygons = feature['geometry']['coordinates']
        for polygon in polygons:
            for coordinate in polygon:
                longitudes.append(coordinate[0])
                latitudes.append(coordinate[1])

    origin = (min(longitudes), min(latitudes))

    # Go through all the points again, this time replace it with new coordinate system
    for i in range(len(geojson['features'])):
        polygons = geojson['features'][i]['geometry']['coordinates']
        for j in range(len(polygons)):
            polygon = polygons[j]
            for k in range(len(polygon)):
                coordinate = polygon[k]
                new_lon = get_great_circle_distance(coordinate[0], coordinate[1], origin[0], coordinate[1])
                new_lat = get_great_circle_distance(coordinate[0], coordinate[1], coordinate[0], origin[1])

                geojson['features'][i]['geometry']['coordinates'][j][k] = [new_lon, new_lat]  # replace the origin coordinates with new ones

    return geojson  # Return new coordinates in [lon, lat] sequence


# Reclassification------------------------------------------------------------------------------------------------------------------
# geojson -> geojson | reclassify the features using "hdb_street" NOTE: this function modifies the original data because of shallow copy
def reclassification(geojson):
    check_level(geojson)
    for i in range(len(geojson['features'])):
        temp = copy.deepcopy(geojson['features'][i]['geometry']['coordinates'])
        all_polygons = get_polygons_in_feature(temp)
        geojson['features'][i]['geometry']['coordinates'] = all_polygons
        geojson['features'][i]['geometry']['type'] = 'Polygon'
    check_level(geojson)


# list[] -> list[list[]] | Extract all polygons in a certain feature and reconstruct them
def get_polygons_in_feature(feature_coordinates):
    all_polygons = []
    # geometries = feature['geometry']['coordinates']

    for i in feature_coordinates:  # This part is the most elegant solution of the entire program. Supported by Luna from Duke-NUS.
        if type(i[0][0]) == float:  # Check if this list is a single polygon
            all_polygons.append(i)  # If so, append it into all_polygons
        else:
            feature_coordinates += i  # If not, append this sub-list into geometries

    return all_polygons


def check_level(geojson):
    flag = True  # 依然是True说明转换成功
    for i in range(8000):
        try:
            len(geojson['features'][i]['geometry']['coordinates'][0][0][0])
            flag = False
        except:
            continue

    if flag:
        print('Processed')
    else:
        print('Raw')


if __name__ == '__main__':
    # res = read_json('data/hdb_struct.geojson')
    res = read_json('smalltest.geojson')

    show_map(res)

    # convertedData = convert_coordinate(res)


