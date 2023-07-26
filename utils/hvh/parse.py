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
    
    def inRange(self,item:"MinMaxValue",offset=10):
        box1 = [[self.x.min-offset,self.y.min-offset],[self.x.min+offset,self.y.min+offset]]
        box2 = [[item.x.min-offset,item.y.min-offset],[item.x.min+offset,item.y.min+offset]]

        return not (box1[0][0] > box2[1][0]
                    or box1[1][0] < box2[0][0]
                    or box1[0][1] > box2[1][1]
                    or box1[1][1] < box2[0][1])
        # return not (self.top_right.x < other.bottom_left.x
        #             or self.bottom_left.x > other.top_right.x
        #             or self.top_right.y < other.bottom_left.y
        #             or self.bottom_left.y > other.top_right.y)

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
    line = '<path style="fill:none;stroke-width:3.996;stroke-linecap:round;stroke-linejoin:round;stroke:rgb(0%,0%,0%);stroke-opacity:1;stroke-miterlimit:10;" d="M 1743.243735 -4062.725643 L 1885.094073 -4062.725643 " transform="matrix(0.12012,0,0,0.11988,0,842)"/>'
    print(line)
    data = getDataByLine(line)
    print(data)
    coords = getMinMaxValuesBySVG(data)
    print(coords)
