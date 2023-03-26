import json

import jsonpickle
from APIResponse import APIResponse, Wall


wall = Wall(fromPosition=0,toPosition=0,isHorizontal=True,isOuterWall=True,doors=[],windows=[])

data = APIResponse(success=True,walls=[wall],junctions=[])

print(jsonpickle.encode(data, unpicklable=False))
