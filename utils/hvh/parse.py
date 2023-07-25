import math
from typing import List
import numpy as np

class MinMax:
    def __init__(self,min:int,max:int):
        self.min = min
        self.max = max
    
class MinMaxValue:
    def __init__(self,minX:int,minY:int,maxX:int,maxY:int):
        self.x = MinMax(minX,maxX)
        self.y = MinMax(minY,maxY)

    def __init__(self,min:List[int],max:List[int]):
        if len(min)!=2:
            raise Exception(f"MinMaxValue needs len(min)=2 - is {len(min)}")
        if len(max)!=2:
            raise Exception(f"MinMaxValue needs len(max)=2 - is {len(max)}")
        
        self.x = MinMax(min[0],max[0])
        self.y = MinMax(min[1],max[1])

    def toSvgData(self):
        return f"M {self.x.min} {self.y.min} L {self.x.max} {self.y.min} L {self.x.max} {self.y.max} L {self.x.min} {self.y.max} Z "
    
    def toDict(self):
        return {"min":{"x":self.x.min,"y":self.y.min},"max":{"x":self.x.max,"y":self.y.max}}
    
    def __str__(self):
        return "[MinMaxValue] " + str(self.toDict())


def getMinMaxValuesBySVG(d:List[str]):
    if d==None:
        return None
    da = d[0].split(" ")

    min = [ 9999999999999999999999, 9999999999999999999999,0]
    max = [-9999999999999999999999,-9999999999999999999999,0]

    temp = [0,0]

    gaps = []

    i = 0

    box = 0

    for item in da:
        if item=="Z":
            box = box + 1

        if not item=="M" and not item=="L" and not item=="Z" and not item=="C" and not item=="":
            i = i + 1

            n = int(float(item))
            itm = 1 if i%2==0 else 0
            temp[itm] = n

            if itm == 1:
                if temp[0] < min[0]:
                    min[0] = temp[0]

                if temp[1] < min[1]:
                    min[1] = temp[1]
                
                if temp[0] > max[0]:
                    max[0] = temp[0]

                if temp[1] > max[1]:
                    max[1] = temp[1]
    
    if len(d)==2 and d[1].startswith("matrix"):
        # https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/transform
        a,b,c,d,e,f = [float(n) for n in d[1].split("(")[1].split(")")[0].split(",")]
        mat = np.array([[ a, c ,e], [ b, d ,f], [ 0, 0 ,0]])
        minVec = np.array([min[0], min[1], 1])
        maxVec = np.array([max[0], max[1], 1])
        min = mat.dot(minVec)
        max = mat.dot(maxVec)
    
    return MinMaxValue(min[:-1],max[:-1])

def getDataByLine(line:str):
    try:
        data = line.split(" d=\"")[1].split("\"")[0]
        transform = ""
        try:
            transform = line.split(" transform=\"")[1].split("\"")[0]
        except:
            pass
        return [data,transform]
    except:
        return None

if __name__=="__main__":
    line = '<path xmlns="http://www.w3.org/2000/svg" style="fill:none;stroke-width:3.996;stroke-linecap:round;stroke-linejoin:round;stroke:rgb(0%,0%,0%);stroke-opacity:1;stroke-miterlimit:10;" d="M 1421.560211 -5282.957511 L 1443.543436 -5282.957511 L 1465.526661 -5286.965429 L 1487.509886 -5292.961014 L 1507.476898 -5298.989184 L 1527.47643 -5308.992687 L 1545.459749 -5320.983857 L 1563.443067 -5333.007611 L 1579.410173 -5349.039284 L 1593.393586 -5363.050705 L 1607.376998 -5381.070045 L 1617.393024 -5399.089384 L 1627.37653 -5419.09639 L 1635.343823 -5439.135981 L 1641.359942 -5461.130654 L 1643.343636 -5483.157912 L 1645.359848 -5507.172836 " transform="matrix(0.12012,0,0,0.11988,0,842)"/>'
    print(line)
    data = getDataByLine(line)
    print(data)
    coords = getMinMaxValuesBySVG(data)
    print(coords)
