import logging
import threading
import time

# import json

# import jsonpickle
# from APIResponse import APIResponse, Wall

# wall = Wall(fromPosition=0,toPosition=0,isHorizontal=True,isOuterWall=True,doors=[],windows=[])

# data = APIResponse(success=True,walls=[wall],junctions=[])

# print(jsonpickle.encode(data, unpicklable=False))

from typing import List
from routes.floorplan.hvh.parse.get import GET,getMinMaxValuesBySVG,getDataByLine

# arr = [
#     getMinMaxValuesBySVG(getDataByLine('<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 341.878906 353.757812 L 341.878906 357.359375 L 345.238281 357.359375 L 345.238281 353.757812 Z M 345.238281 382.320312 L 341.878906 382.320312 L 341.878906 385.917969 L 345.238281 385.917969 L 345.238281 382.320312 "/>')),
#     getMinMaxValuesBySVG(getDataByLine('<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 316.921875 385.917969 L 295.558594 385.917969 L 295.558594 389.28125 L 316.921875 389.28125 Z M 338.28125 385.917969 L 338.28125 389.28125 L 349.078125 389.28125 L 349.078125 385.917969 L 338.28125 385.917969 "/>')),
#     getMinMaxValuesBySVG(getDataByLine('<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 175.078125 353.757812 L 288.839844 353.757812 L 288.839844 347.039062 L 175.078125 347.039062 Z M 175.078125 353.757812 "/>')),
#     getMinMaxValuesBySVG(getDataByLine('<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 366.839844 159 L 366.839844 194.519531 L 369.960938 194.519531 L 369.960938 159 Z M 369.960938 216.121094 L 366.839844 216.121094 L 366.839844 247.800781 L 369.960938 247.800781 L 369.960938 216.121094 "/>')),
#     getMinMaxValuesBySVG(getDataByLine('<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 306.121094 152.28125 L 168.359375 152.28125 L 168.359375 159 L 306.121094 159 Z M 334.921875 159 L 416.039062 159 L 416.039062 152.28125 L 334.921875 152.28125 L 334.921875 159 "/>')),
#     getMinMaxValuesBySVG(getDataByLine('<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 288.839844 254.757812 L 409.320312 254.757812 L 409.320312 247.800781 L 288.839844 247.800781 Z M 288.839844 254.757812 "/>')),
#     getMinMaxValuesBySVG(getDataByLine('<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 341.878906 353.757812 L 409.320312 353.757812 L 409.320312 347.039062 L 341.878906 347.039062 Z M 341.878906 353.757812 "/>')),
#     getMinMaxValuesBySVG(getDataByLine('<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 168.359375 449.519531 L 323.878906 449.519531 L 323.878906 442.558594 L 168.359375 442.558594 Z M 345.480469 442.558594 L 345.480469 449.519531 L 416.039062 449.519531 L 416.039062 442.558594 L 345.480469 442.558594 "/>')),
#     getMinMaxValuesBySVG(getDataByLine('<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 416.039062 385.679688 L 416.039062 290.519531 L 409.320312 290.519531 L 409.320312 385.679688 Z M 416.039062 442.558594 L 416.039062 407.28125 L 409.320312 407.28125 L 409.320312 442.558594 Z M 416.039062 258.121094 L 416.039062 216.121094 L 409.320312 216.121094 L 409.320312 258.121094 Z M 409.320312 194.519531 L 416.039062 194.519531 L 416.039062 159 L 409.320312 159 L 409.320312 194.519531 "/>')),
#     getMinMaxValuesBySVG(getDataByLine('<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 168.359375 237.238281 L 168.359375 272.519531 L 175.078125 272.519531 L 175.078125 237.238281 Z M 168.359375 180.359375 L 175.078125 180.359375 L 175.078125 159 L 168.359375 159 Z M 168.359375 329.28125 L 168.359375 364.320312 L 175.078125 364.320312 L 175.078125 329.28125 Z M 175.078125 421.441406 L 168.359375 421.441406 L 168.359375 442.558594 L 175.078125 442.558594 L 175.078125 421.441406 "/>')),
#     getMinMaxValuesBySVG(getDataByLine('<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 349.078125 442.558594 L 352.199219 442.558594 L 352.199219 385.917969 L 349.078125 385.917969 Z M 349.078125 442.558594 "/>')),
#     getMinMaxValuesBySVG(getDataByLine('<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 295.558594 357.359375 L 295.558594 283.320312 L 288.839844 283.320312 L 288.839844 357.359375 Z M 295.558594 258.121094 L 295.558594 254.757812 L 288.839844 254.757812 L 288.839844 258.121094 Z M 295.558594 442.558594 L 295.558594 382.320312 L 288.839844 382.320312 L 288.839844 442.558594 L 295.558594 442.558594 "/>')),

#     getMinMaxValuesBySVG(getDataByLine('<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 307.320312 147.71875 L 163.800781 147.71875 L 163.800781 152.28125 L 307.320312 152.28125 Z M 333.71875 147.71875 L 333.71875 152.28125 L 420.601562 152.28125 L 420.601562 147.71875 L 333.71875 147.71875 "/>')),
#     getMinMaxValuesBySVG(getDataByLine('<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 163.800781 454.078125 L 325.078125 454.078125 L 325.078125 449.519531 L 163.800781 449.519531 Z M 344.28125 449.519531 L 344.28125 454.078125 L 420.601562 454.078125 L 420.601562 449.519531 L 344.28125 449.519531 "/>')),
#     getMinMaxValuesBySVG(getDataByLine('<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 420.601562 386.878906 L 420.601562 289.320312 L 416.039062 289.320312 L 416.039062 386.878906 Z M 420.601562 152.28125 L 416.039062 152.28125 L 416.039062 195.480469 L 420.601562 195.480469 Z M 416.039062 214.917969 L 416.039062 259.320312 L 420.601562 259.320312 L 420.601562 214.917969 Z M 420.601562 406.078125 L 416.039062 406.078125 L 416.039062 449.519531 L 420.601562 449.519531 L 420.601562 406.078125 "/>')),
#     getMinMaxValuesBySVG(getDataByLine('<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 420.601562 386.878906 L 420.601562 289.320312 L 416.039062 289.320312 L 416.039062 386.878906 Z M 420.601562 152.28125 L 416.039062 152.28125 L 416.039062 195.480469 L 420.601562 195.480469 Z M 416.039062 214.917969 L 416.039062 259.320312 L 420.601562 259.320312 L 420.601562 214.917969 Z M 420.601562 406.078125 L 416.039062 406.078125 L 416.039062 449.519531 L 420.601562 449.519531 L 420.601562 406.078125 "/>')),
#     getMinMaxValuesBySVG(getDataByLine('<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 163.800781 236.039062 L 163.800781 273.480469 L 168.359375 273.480469 L 168.359375 236.039062 Z M 163.800781 449.519531 L 168.359375 449.519531 L 168.359375 420.238281 L 163.800781 420.238281 Z M 168.359375 365.519531 L 168.359375 328.078125 L 163.800781 328.078125 L 163.800781 365.519531 Z M 163.800781 181.320312 L 168.359375 181.320312 L 168.359375 152.28125 L 163.800781 152.28125 L 163.800781 181.320312 "/>')),
# ]

# for item in arr:
#     # M 163.800781 236.039062 L 163.800781 273.480469 L 168.359375 273.480469 L 168.359375 236.039062 Z M 163.800781 449.519531 L 168.359375 449.519531 L 168.359375 420.238281 L 163.800781 420.238281 Z M 168.359375 365.519531 L 168.359375 328.078125 L 163.800781 328.078125 L 163.800781 365.519531 Z M 163.800781 181.320312 L 168.359375 181.320312 L 168.359375 152.28125 L 163.800781 152.28125 L 163.800781 181.320312 
#     print(f'<path style=" stroke:none;fill-rule:nonzero;fill:rgb(0%,100%,0%);fill-opacity:1;" d="M {item["min"][0]} {item["min"][1]} L {item["max"][0]} {item["min"][1]} L {item["max"][0]} {item["max"][1]} L {item["min"][0]} {item["max"][1]} Z "/>')

# print(arr)

# GET({},{},{})












# class PipelineStep:
#     def __init__(self,func) -> None:
#         self.func = func
#         self.running = False
#         self.finished = False
#         self.result = {}
    
#     def run(self):
#         self.running = True
#         self.result = self.func()
#         self.running = False
#         self.finished = True


# class Pipeline:
#     def thread_function(s,e):
#         while s._run_thread:
#             if len(s.steps)>0 and s.steps[0].running==False:
#                 s.steps[0].run()

#     def __init__(self) -> None:
#         global _run_thread
#         self.steps:List[PipelineStep] = []
#         self._run_thread = True
#         self._thread = threading.Thread(target=self.thread_function,args=(self,))
#         self._thread.start()

#     def stop(self):
#         self._run_thread = False
#         self._thread.stop()

#     def add(self,step:PipelineStep) -> None:
#         self.steps.append(step)

#     def get(self):
#         item = self.steps.pop(0)

#         item.run()

#         return item
    
# def myTestFunc()->str:
#     print(f"[myTestFunc]")
#     time.sleep(1)

# pipeline = Pipeline()
# for i in range(10):
#     step = PipelineStep(myTestFunc)
#     pipeline.add(step)
