import numpy as np
from local_libs.private_tool import *
import os

currDir = os.path.dirname(os.path.realpath(__file__))

ls = loadJson(f"{currDir}/signal.json")
print(ls[2])