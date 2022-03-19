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
    data = read_json('data/hdb_carbon.geojson')
    write_json(data)
    # data1 = copy.deepcopy(data)  # Because the following function will modify the original data
    # test = generate_convex_hull_geojson(data1)


if __name__ == '__main__':
    main()
