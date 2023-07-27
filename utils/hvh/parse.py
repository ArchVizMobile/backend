from typing import List
import numpy as np

class MinMax:
    def __init__(self,min:int,max:int):
        self.min = min
        self.max = max
    
class MinMaxValue:
    def __init__(self,minX:int,minY:int,maxX:int,maxY:int,corrected:bool,raw:str):
        self.x = MinMax(minX,maxX)
        self.y = MinMax(minY,maxY)
        self.corrected = corrected
        self.raw = raw

    def __init__(self,min:List[int],max:List[int],corrected:bool,raw:str):
        if len(min)!=2:
            raise Exception(f"MinMaxValue needs len(min)=2 - is {len(min)}")
        if len(max)!=2:
            raise Exception(f"MinMaxValue needs len(max)=2 - is {len(max)}")
        
        self.x = MinMax(min[0],max[0])
        self.y = MinMax(min[1],max[1])
        self.corrected = corrected
        self.raw = raw

    def toSvgData(self):
        return f"M {self.x.min} {self.y.min} L {self.x.max} {self.y.min} L {self.x.max} {self.y.max} L {self.x.min} {self.y.max} Z "
    
    def toDict(self):
        return {
            "min": {
                "x": self.x.min,
                "y": self.y.min
            },
            "max": {
                "x": self.x.max,
                "y": self.y.max
            },
            "corrected": self.corrected,
            "raw": self.getCorrected()
        }
    
    def getCorrected(self):
        ret = []
        
        if not self.corrected:
            return self.raw.split("d=\"")[1].split("\"")[0]

        matrix = self.raw.split("transform=\"")[1].split("\"")[0]
        # print(matrix)
        mat = getMatrixFromString(matrix)

        n = 0
        last = -1

        for item in self.raw.split("d=\"")[1].split("\"")[0].split(" "):
            try:
                i = float(item)
                if n == 0:
                    n = 1
                    last = i
                elif n == 1:
                    n = 0
                    dat = matrixTransformByMatrix(mat,last,i)
                    ret.append(str(dat[0]))
                    ret.append(str(dat[1]))


            except:
                ret.append(item)
        ret = " ".join(ret)
        return ret

    def __str__(self):
        return f"[MinMaxValue] {str(self.toDict())}"
    
def getMinMaxValuesBySVG(d:List[str],raw:str):
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
    
    corrected = False
    if len(d)==2 and d[1]!=None and d[1].startswith("matrix"):
        corrected = True
        mat = getMatrixFromString(d[1])
        min = matrixTransformByMatrix(mat,min[0], min[1])
        max = matrixTransformByMatrix(mat,max[0], max[1])
    
    return MinMaxValue(min[:-1],max[:-1],corrected,raw)

class Point:
    def __init__(self,x:float,y:float) -> None:
        self.x = x
        self.y = y
    
    def __str__(self) -> str:
        return f"Point(x={self.x}, y={self.y})"
    
    def __repr__(self) -> str:
        return f"Point(x={self.x}, y={self.y})"

class Point3D(Point):
    def __init__(self, x: float, y: float,z: float=0) -> None:
        super().__init__(x, y)
        self.z = z

    def __str__(self) -> str:
        return f"Point(x={self.x}, y={self.y}, z={self.z})"
    
    def __repr__(self) -> str:
        return f"Point(x={self.x}, y={self.y}, z={self.z})"

class Opening:
    def __init__(self,fr:Point,to:Point) -> None:
        self.fr = fr
        self.to = to

class WallData(MinMaxValue):
    def __init__(self, min: List[int], max: List[int], corrected: bool, raw: str,openings:List[Opening]):
        super().__init__(min, max, corrected, raw)
        self.openings = openings

class Box:
    def __init__(self,points:List[Point]) -> None:
        self.points = points
        self.min = Point(9999999999999999999,9999999999999999999)
        self.max = Point(-9999999999999999999,-9999999999999999999)
        for point in self.points:
            if point.x < self.min.x:
                self.min.x = point.x
            if point.y < self.min.y:
                self.min.y = point.y

            if point.x > self.max.x:
                self.max.x = point.x
            if point.y > self.max.y:
                self.max.y = point.y

    def __repr__(self) -> str:
        return f"Box(from: x={self.min.x}, y={self.min.y} | to: x={self.max.x}, y={self.max.y})"

class Feature:
    def __init__(self,fr:Point3D,to:Point3D,cls:str) -> None:
        self.fr = fr
        self.to = to
        self.cls = cls

class Window(Feature):
    def __init__(self, fr: Point3D, to: Point3D,cls:str) -> None:
        super().__init__(fr, to)

class Door(Feature):
    def __init__(self, fr: Point3D, to: Point3D,cls:str) -> None:
        super().__init__(fr, to)

class Gap:
    def __init__(self, fr: Point, to: Point) -> None:
        self.fr = fr
        self.to = to

    def __str__(self) -> str:
        return f"Gap(from x={self.fr.x}, y={self.fr.y} | to x={self.to.x}, y={self.to.y})"
    
    def __repr__(self) -> str:
        return f"Gap(from x={self.fr.x}, y={self.fr.y} | to x={self.to.x}, y={self.to.y})"

class Wall:
    def __init__(self,boxes: List[Box]) -> None:
        self.boxes = boxes
        self.min = Point(9999999999999999999,9999999999999999999)
        self.max = Point(-9999999999999999999,-9999999999999999999)
        for box in self.boxes:
            if box.min.x < self.min.x:
                self.min.x = box.min.x
            if box.min.y < self.min.y:
                self.min.y = box.min.y

            if box.max.x > self.max.x:
                self.max.x = box.max.x
            if box.max.y > self.max.y:
                self.max.y = box.max.y
        
        self.isHorizontal = self.max.x - self.min.x > self.max.y - self.min.y

        self.gaps:List[Gap] = []

        if self.isHorizontal:
            self.boxes = sorted(self.boxes,key=lambda k: k.min.x)
        else:
            self.boxes = sorted(self.boxes,key=lambda k: k.min.y)

        n = 0
        last = None
        for item in self.boxes:
            if n==0:
                n=1
                last = item
            elif n==1:
                n=0
                self.gaps.append(Gap(Point(item.min.x,last.max.y),Point(item.max.x,item.min.y)))
        
        self.windows:List[Window] = []
        self.doors:List[Door] = []
    
    def hasGap(self,fr:Point,to:Point,offset=5):
        box1 = Gap(Point(fr.x-offset,fr.y-offset),Point(to.x+offset,to.y+offset))

        for gap in self.gaps:
            x = not (box1.fr.x > gap.to.x
                or box1.to.x < gap.fr.x
                or box1.fr.y > gap.to.y
                or box1.to.y < gap.fr.y)
            if x:
                return gap
        return None
    
    def addDoor(self,door:Door)->None:
        self.doors.append(door)

    def addWindow(self,window:Window)->None:
        self.windows.append(window)

    def __repr__(self) -> str:
        return f"Wall(Position(from: x={self.min.x}, y={self.min.y} | to: x={self.max.x}, y={self.max.y}) | horizontal={self.isHorizontal} | doors={len(self.doors)} | windows={len(self.windows)})" #  {self.gaps}
    
def getWallInformationBySVG(raw:str):
    data,matrix = getDataByLine(raw)

    if data==None:
        return None
    
    boxes = []
    try:
        for box in data.split(" Z "):
            points = []

            for pts in box.split("M ")[1].split(" L "):
                p = pts.split(" ")
                points.append(Point(float(p[0]),float(p[1])))
            boxes.append(Box(points))
        wall = Wall(boxes)
        return wall
    except:
        return None

# https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/transform
def getMatrixFromString(matrix:str):
    a,b,c,d,e,f = [float(n) for n in matrix.split("(")[1].split(")")[0].split(",")]
    mat = np.array([[ a, c ,e], [ b, d ,f], [ 0, 0 ,0]])
    return mat

def matrixTransformByMatrix(mat,x:float,y:float):
    vec = np.array([x, y, 1])
    return mat.dot(vec)

def matrixTransformByString(matrix:str,x:float,y:float):
    mat = getMatrixFromString(matrix)
    vec = np.array([x, y, 1])
    return mat.dot(vec)

def getDataByLine(line:str):
    try:
        data = getAttributeDataFromSvg(line,"d")
        transform = ""
        try:
            transform = getAttributeDataFromSvg(line,"transform")
        except:
            pass
        return data,transform
    except:
        return None,None

def getAttributeDataFromSvg(svg:str,attribute:str):
    try:
        return svg.split(" "+attribute+"=\"")[1].split("\"")[0]
    except:
        return None

if __name__=="__main__":
    # line = '<path style="fill:none;stroke-width:3.996;stroke-linecap:round;stroke-linejoin:round;stroke:rgb(0%,0%,0%);stroke-opacity:1;stroke-miterlimit:10;" d="M 1743.243735 -4062.725643 L 1885.094073 -4062.725643 " transform="matrix(0.12012,0,0,0.11988,0,842)"/>'
    line = '<path style=" stroke:none;fill-rule:nonzero;fill:rgb(83.59375%,83.59375%,83.59375%);fill-opacity:1;" d="M 163.800781 236.039062 L 163.800781 273.480469 L 168.359375 273.480469 L 168.359375 236.039062 Z M 163.800781 449.519531 L 168.359375 449.519531 L 168.359375 420.238281 L 163.800781 420.238281 Z M 168.359375 365.519531 L 168.359375 328.078125 L 163.800781 328.078125 L 163.800781 365.519531 Z M 163.800781 181.320312 L 168.359375 181.320312 L 168.359375 152.28125 L 163.800781 152.28125 L 163.800781 181.320312 "/>'
    wall = getWallInformationBySVG(line)
    found,position = wall.hasGap(Point(160, 180), Point(170, 240))
    if found:
        print(found)
        print(position)
        wall.addDoor(Door(position.fr,position.to))
    print(wall)
