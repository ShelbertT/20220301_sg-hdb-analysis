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


def main():
    original_data = read_json('data/hdb_carbon.geojson')
    data = copy.deepcopy(original_data)  # Because the following function will modify the original data

    convex_hull = generate_convex_hull_geojson(data)
    show_map(convex_hull)


def test():
    res = read_json('smalltest.geojson')
    # show_map(res)

    res1 = generate_convex_hull_geojson(res)
    show_map(res1)


if __name__ == '__main__':
    # test()
    main()
