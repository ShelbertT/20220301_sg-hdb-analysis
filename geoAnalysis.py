import copy
from visualization import *
from rawProcessing import *
from getConvexHull import *
from geoAnalysis import *


# list[list[x, y]] -> double | calculate the area of a polygon based on its [converted coords]
def get_shape_area(polygon):
    # Calculation is based on [Shoelace Theorem]
    area = 0
    for i in range(len(polygon)):
        current = i
        if current == len(polygon) - 1:
            next_one = 0
        else:
            next_one = i + 1
        area += (polygon[current][0] * polygon[next_one][1]) - (polygon[next_one][0] * polygon[current][1])

    area = abs(area) / 2
    return area


# list[list[x, y]] -> double | calculate the perimeter of a polygon based on its [converted coords]
def get_shape_length(polygon):
    perimeter = 0
    for i in range(len(polygon)):
        start = i
        if start == len(polygon) - 1:
            end = 0
        else:
            end = i + 1

        this_line = math.sqrt(
            math.pow((polygon[start][0] - polygon[end][0]), 2) + math.pow((polygon[start][1] - polygon[end][1]), 2))
        perimeter += this_line

    return perimeter


# list[list[x, y]], double -> double | Calculate the surface area of a building. All units in meters
def get_surface_area(polygon, height):
    # roof_area = get_shape_area(polygon)
    shape_length = get_shape_length(polygon)
    surface_area = height * shape_length
    return surface_area


# geojson -> geojson | Extract all polygons
def extract_precinct(geojson):
    precinct = GeoJSON(name='precinct')
    all_new_feature_names = []

    for feature in geojson['features']:
        street_name = feature["properties"]["HDB_cleaning.hdb_street"]
        feature_name = street_name.replace(" ", "_").replace('\'', '')  # ID cannot contain '\'', so it has to be different from street_name

        if feature_name not in all_new_feature_names:
            properties = Properties(hdb_street=street_name)  # Creat an instance
            exec(f'{feature_name} = Feature(polygons=feature["geometry"]["coordinates"], feature_id=feature_name, properties=properties.all)')  # Creat an instance using the street_name as new_feature_name
            all_new_feature_names.append(feature_name)

        elif feature_name in all_new_feature_names:
            polygons = feature["geometry"]["coordinates"]
            exec(f'{feature_name}.add_polygons(polygons)')

    for new_feature_name in all_new_feature_names:
        exec(f'precinct.add_feature({new_feature_name})')

    return precinct.geojson


# polygons[polygon[coords[x, y]]] -> list[coords[x, y]]  # input a group of polygons, return all their vertices
def extract_all_vertices(polygons):
    vertices = []
    for polygon in polygons:
        for vertex in polygon:
            if vertex not in vertices:
                vertices.append(vertex)

    return vertices


if __name__ == '__main__':
    main()
