import folium
import webbrowser
import turtle
import math

# Folium does not support display map in pycharm directly, so a class was created to help display the map in a browser.
# Chrome is recommended.
# This part of solution comes from stackoverflow: https://stackoverflow.com/questions/36969991/folium-map-not-displaying


class Map:
    def __init__(self, location, zoom_start=1):  # Define the attributes
        self.location = location
        self.zoom_start = zoom_start
        self.instance = folium.Map(location=self.location, zoom_start=self.zoom_start)  # Create the map

    def show_map(self):  # Define a function
        self.instance.save("map.html")  # Display the map
        webbrowser.open("map.html")

    def add_geojson(self, geojson, name):  # Allowing adding GeoJSON into display
        folium.GeoJson(geojson, name=name).add_to(self.instance)


def show_map(geojson):
    m = Map(location=[1.3721211, 103.8458177], zoom_start=14)
    m.add_geojson(geojson, 'singapore')
    m.show_map()


def draw_map(polygons):
    all_lon = []
    all_lat = []
    for polygon in polygons:
        # print(polygon)
        for coordinate in polygon:
            all_lon.append(coordinate[0])
            all_lat.append(coordinate[1])
            # print(coordinate)
    canvas_width = math.ceil((max(all_lon) - min(all_lon))/15)
    canvas_height = math.ceil((max(all_lat) - min(all_lat))/15)
    print(canvas_height, canvas_width)

    turtle.setup(width=canvas_width, height=canvas_height)
    turtle.done()


# if __name__ == '__main__':
