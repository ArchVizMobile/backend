import glob
import os
import time
import random
from typing import List
from PIL import Image, ImageChops
import jsonpickle
import pymongo
from config import CONFIG

from routes.floorplan.hvh.parse.get import Color, getFooter, getHeaderBar
from runPipeline import runPipeline
from utils.hvh.parse import Door, Gap, MinMaxValue, Point, Point3D, Wall, Window, getAttributeDataFromSvg, getDataByLine, getWallInformationBySVG

dir = glob.glob("uploaded/*.pdf")
file = dir[random.randint(0, len(dir)-1)].replace('\\','/')

# file = "uploaded/Calvus 631.pdf"

header_bar = Color("87.889099%,92.576599%,96.484375%")
outer_wall = Color("83.59375%,83.59375%,83.59375%")
inner_wall = Color("50%,50%,50%")
inner_wall_2 = Color("49.609375%,49.609375%,49.609375%")
input_field = Color("96.875%,96.875%,96.875%")
table_heading = Color("88.28125%,88.28125%,88.28125%")
entry = Color("39.501953%,39.501953%,39.501953%")
footerHeightOffset = 10

IMAGE_SCALE_FACTOR = 4
TARGET_DOOR_WIDTH = 113

class Furniture:
    def __init__(self,fr:Point,to:Point,obj:str) -> None:
        self.fr = fr
        self.to = to
        self.obj = obj

class Floorplan:
    def __init__(self,
            image:str,
            svg:List[str],
            bbox:tuple[int, int, int, int],
            header:MinMaxValue,
            height:float,
            width:float,
            maxHeight:int) -> None:
        self.image = image
        self.svg = svg
        self.bbox = bbox
        self.header = header
        self.height = height
        self.width = width
        self.maxHeight = maxHeight
        self.walls:List[Wall] = []
        self.furniture:List[Furniture] = []

        for line in svg:
            if inner_wall.check(line) or inner_wall_2.check(line):
                wall = getWallInformationBySVG(line)
                if wall!=None:
                    self.walls.append(wall)

    def __repr__(self) -> str:
        return f"Floorplan({self.image})"
    
    def addFurniture(self,furniture:Furniture):
        self.furniture.append(furniture)

def generateSVGs(file:str):
    baseName = file.split(".")[0].split("/")[1]
    print(f"[{baseName}] Parsing SVGs from PDF")
    os.system(f'mkdir "uploaded/{baseName}"')
    os.system(f'pdf2svg\dist-64bits\pdf2svg.exe "{file}" "uploaded/{baseName}/%d.svg" all')
    svgs = glob.glob(f"uploaded/{baseName}/*.svg")
    print(f"[{baseName}] Creating Images from SVGs")
    for svgidx,svg in enumerate(svgs):
        with open(svg) as file_handle:
            lines = file_handle.read().split("\n")
            width = getAttributeDataFromSvg(lines[1],"width").removesuffix("pt")
            height = getAttributeDataFromSvg(lines[1],"height").removesuffix("pt")
            print(f"[{baseName}] {svgidx+1}/{len(svgs)}")
            cmd = f'ImageMagick\convert.exe -size {float(width)*IMAGE_SCALE_FACTOR}x{float(height)*IMAGE_SCALE_FACTOR} "{svg}" "uploaded/{baseName}/{svgidx+1}.png"'
            # print(cmd)
            os.system(cmd)
    return svgs,[f.replace(".svg",".png") for f in svgs]

def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox),bbox
    else: 
        # Failed to find the borders, convert to "RGB"        
        return trim(im.convert('RGB'))

def GenerateFloorplans(pdf:str):
    svgs,pngs = generateSVGs(pdf)

    floorplans:List[Floorplan] = []

    for idx,svg in enumerate(svgs):
        with open(svg) as file_handler:
            lines = file_handler.read().split("\n")

            found = 0
            for line in lines:
                if inner_wall.check(line) or outer_wall.check(line):
                    found = found + 1

            if found > 1 and idx>2:
                header = getHeaderBar(lines)

                height = 842.
                try:
                    height = float(getAttributeDataFromSvg(lines[1],"height").removesuffix("pt"))
                except:
                    pass

                width = 595.
                try:
                    width = float(getAttributeDataFromSvg(lines[1],"width").removesuffix("pt"))
                except:
                    pass

                maxHeight = height - 30
                footer = getFooter(lines)
                if footer!=None:
                    maxHeight = footer.y.min

                im = Image.open(pngs[idx])
                im1 = im.crop((
                    0,  #left
                    (header.y.max+IMAGE_SCALE_FACTOR)*IMAGE_SCALE_FACTOR, #top
                    im.width, #right
                    maxHeight*IMAGE_SCALE_FACTOR #bottom
                ))
                im1,bbox = trim(im1)
                newFile = pngs[idx].replace(".png",".2.png")
                im1.save(newFile)
                # print(f"{idx+1}.svg | maxHeight={maxHeight} header.y.max={header.y.max}")
                floorplans.append(Floorplan(newFile,lines,bbox,header,height,width,maxHeight))

    return floorplans,svgs,pngs

class Timer:
    def __init__(self,name:str) -> None:
        self.start = time.time()
        self.name = name
        pass

    def __str__(self):
        end = time.time()
        return (f"[{self.name} Timer] Took ~{round(end-self.start)}s")

generate_timer = Timer("Generate")
together_timer = Timer("Together")
floorplans,svgs,pngs = GenerateFloorplans(file)
print(generate_timer) # ~9s

images = [plan.image for plan in floorplans]
# images = ['uploaded/Calvus 631\\4.2.png', 'uploaded/Calvus 631\\5.2.png']
# print(images)

detect_timer = Timer("Detect")

out = runPipeline(images)

def getPointsByItem(item,idx):
    xplus = (floorplans[idx].bbox[0])
    yplus = ((floorplans[idx].header.y.max+IMAGE_SCALE_FACTOR)*IMAGE_SCALE_FACTOR + floorplans[idx].bbox[1])
    return Point(
        (item.xmin+xplus)/IMAGE_SCALE_FACTOR,
        (item.ymin+yplus)/IMAGE_SCALE_FACTOR
    ), Point(
        (item.xmax+xplus)/IMAGE_SCALE_FACTOR,
        (item.ymax+yplus)/IMAGE_SCALE_FACTOR
    ), item.object

for idx,floor in enumerate(out):
    # print(f"stairs={floor['stairs']}\n")
    # print(f"wallfeatures={floor['wallfeatures']}\n")
    # print(f"wallfeatures.window={floor['wallfeatures'].window}\n")
    # print(f"furniture={floor['furniture']}\n")

    if floor['wallfeatures'].window!=None:
        for window in floor['wallfeatures'].window:
            fr,to,obj = getPointsByItem(window,idx)
            for wall in floorplans[idx].walls:
                gap = wall.hasGap(fr,to)
                if gap!=None:
                    wall.addWindow(Window(gap.fr,gap.to,obj))

    if floor['wallfeatures'].door!=None:
        for door in floor['wallfeatures'].door:
            fr,to,obj = getPointsByItem(door,idx)
            for wall in floorplans[idx].walls:
                gap = wall.hasGap(fr,to)
                if gap!=None:
                    wall.addDoor(Door(gap.fr,gap.to,obj))

    if floor['wallfeatures'].doubleDoor!=None:
        for door in floor['wallfeatures'].doubleDoor:
            fr,to,obj = getPointsByItem(door,idx)
            for wall in floorplans[idx].walls:
                gap = wall.hasGap(fr,to)
                if gap!=None:
                    wall.addDoor(Door(gap.fr,gap.to,obj))

    # Furniture

    if floor['furniture'].armchair!=None:
        for furniture in floor['furniture'].armchair:
            fr,to,obj = getPointsByItem(furniture,idx)
            floorplans[idx].addFurniture(Furniture(fr,to,obj))

    if floor['furniture'].bathtub!=None:
        for furniture in floor['furniture'].bathtub:
            fr,to,obj = getPointsByItem(furniture,idx)
            floorplans[idx].addFurniture(Furniture(fr,to,obj))

    if floor['furniture'].bed!=None:
        for furniture in floor['furniture'].bed:
            fr,to,obj = getPointsByItem(furniture,idx)
            floorplans[idx].addFurniture(Furniture(fr,to,obj))

    if floor['furniture'].couch!=None:
        for furniture in floor['furniture'].couch:
            fr,to,obj = getPointsByItem(furniture,idx)
            floorplans[idx].addFurniture(Furniture(fr,to,obj))

    if floor['furniture'].desk!=None:
        for furniture in floor['furniture'].desk:
            fr,to,obj = getPointsByItem(furniture,idx)
            floorplans[idx].addFurniture(Furniture(fr,to,obj))

    if floor['furniture'].dining_table_4_chairs!=None:
        for furniture in floor['furniture'].dining_table_4_chairs:
            fr,to,obj = getPointsByItem(furniture,idx)
            floorplans[idx].addFurniture(Furniture(fr,to,obj))

    if floor['furniture'].dining_table_6_chairs!=None:
        for furniture in floor['furniture'].dining_table_6_chairs:
            fr,to,obj = getPointsByItem(furniture,idx)
            floorplans[idx].addFurniture(Furniture(fr,to,obj))

    if floor['furniture'].kitchenette!=None:
        for furniture in floor['furniture'].kitchenette:
            fr,to,obj = getPointsByItem(furniture,idx)
            floorplans[idx].addFurniture(Furniture(fr,to,obj))

    if floor['furniture'].lowboardTV!=None:
        for furniture in floor['furniture'].lowboardTV:
            fr,to,obj = getPointsByItem(furniture,idx)
            floorplans[idx].addFurniture(Furniture(fr,to,obj))

    if floor['furniture'].masterbed!=None:
        for furniture in floor['furniture'].masterbed:
            fr,to,obj = getPointsByItem(furniture,idx)
            floorplans[idx].addFurniture(Furniture(fr,to,obj))

    if floor['furniture'].shelf!=None:
        for furniture in floor['furniture'].shelf:
            fr,to,obj = getPointsByItem(furniture,idx)
            floorplans[idx].addFurniture(Furniture(fr,to,obj))

    if floor['furniture'].shower!=None:
        for furniture in floor['furniture'].shower:
            fr,to,obj = getPointsByItem(furniture,idx)
            floorplans[idx].addFurniture(Furniture(fr,to,obj))

    if floor['furniture'].sink!=None:
        for furniture in floor['furniture'].sink:
            fr,to,obj = getPointsByItem(furniture,idx)
            floorplans[idx].addFurniture(Furniture(fr,to,obj))

    if floor['furniture'].table!=None:
        for furniture in floor['furniture'].table:
            fr,to,obj = getPointsByItem(furniture,idx)
            floorplans[idx].addFurniture(Furniture(fr,to,obj))

    if floor['furniture'].wc!=None:
        for furniture in floor['furniture'].wc:
            fr,to,obj = getPointsByItem(furniture,idx)
            floorplans[idx].addFurniture(Furniture(fr,to,obj))

print(detect_timer)
response_timer = Timer("Response")

TARGET_CEILING_HEIGHT = 300

SCALE = 1
entry_json = {
    "top": 0,
    "left": 0,
    "height": 0,
    "width": 0,
}

entries:List[Wall] = []
for plan in floorplans:
    for line in plan.svg:
        if entry.check(line):
            wall = getWallInformationBySVG(line)
            # print(line)
            # print(wall)
            entries.append(wall)

# print(entries)

foundEntries = {}
for entry in entries:
    for plan in floorplans:
        for walls in plan.walls:
            gap = walls.hasGap(Point(entry.min.x,entry.min.y),Point(entry.max.x,entry.max.y),10)
            if gap!=None:
                if gap.__str__() not in foundEntries:
                    for d in walls.doors:
                        if d.fr.x == gap.fr.x and d.fr.y == gap.fr.y and d.to.x == gap.to.x and d.to.y == gap.to.y:
                            foundEntries[gap.__str__()] = gap


entry_gap:Gap = foundEntries[list(foundEntries.keys())[0]]
if entry_gap.to.x - entry_gap.fr.x > entry_gap.to.y - entry_gap.fr.y:
    # Hozizontal
    SCALE = TARGET_DOOR_WIDTH/(entry_gap.to.x - entry_gap.fr.x)
else:
    SCALE = TARGET_DOOR_WIDTH/(entry_gap.to.y - entry_gap.fr.y)

entry_json = {
    "top": entry_gap.fr.y*SCALE,
    "left": entry_gap.to.x*SCALE,
    "height": entry_gap.to.y-entry_gap.fr.y*SCALE,
    "width": entry_gap.fr.x-entry_gap.to.x*SCALE,
}

response = {
  "success": True,
  "name": f"Grundriss von {file} generiert am {time.strftime('%X %x')}",
  "walls": [],
  "junctions": [],
  "entry":entry_json,
  "rooms": [],
  "furniture": [],
  "scale": SCALE,
#   "stories": len(floorplans)
}

min = [99999999999999999999999,99999999999999999999999]
max = [-99999999999999999999999,-99999999999999999999999]

n = 0
# print(floorplans)
for idx,plan in enumerate(floorplans):
    # print(len(plan.walls))
    for wall in plan.walls:

        if wall.min.x < min[0]:
            min[0] = wall.min.x
        if wall.min.y < min[1]:
            min[1] = wall.min.y

        if wall.max.x > max[0]:
            max[0] = wall.max.x
        if wall.max.y > max[1]:
            max[1] = wall.max.y

        n = n + 1
        w = {
            "fromPosition": {
                "x": wall.min.x*SCALE,
                "y": wall.min.y*SCALE
            },
            "toPosition": {
                "x": (wall.min.x if not wall.isHorizontal else wall.max.x)*SCALE,
                "y": ((wall.max.y if not wall.isHorizontal else wall.min.y))*SCALE
            },
            "isHorizontal": wall.isHorizontal,
            "isOuterWall": False,
            "features": [],
            "gaps": [],
            "depth": (wall.max.y-wall.min.y if  wall.isHorizontal else wall.max.x-wall.min.x)*SCALE,
            "height": TARGET_CEILING_HEIGHT,
            "startHeight": TARGET_CEILING_HEIGHT*idx
        }
        # if(len(wall.doors)>0):
            # print(wall.doors)
        # if(len(wall.windows)>0):
            # print(wall.windows)
        for feature in wall.gaps:
            if wall.isHorizontal:
                fromPosition = (feature.fr.x - wall.min.x)
                toPosition = (feature.to.x - wall.min.x)
            else:
                fromPosition = feature.fr.y - wall.min.y
                toPosition = feature.to.y - wall.min.y

            w["gaps"].append({
                "fromPosition":fromPosition*SCALE,
                "toPosition":toPosition*SCALE
            })
        for feature in wall.doors:
            if wall.isHorizontal:
                fromPosition = (feature.fr.x - wall.min.x)
                toPosition = (feature.to.x - wall.min.x)
            else:
                fromPosition = feature.fr.y - wall.min.y
                toPosition = feature.to.y - wall.min.y

            # print(feature)
            w["features"].append({
                "fromPosition": fromPosition*SCALE,
                "toPosition": toPosition*SCALE,
                "hinge": -1,
                "openLeft": False,
                "style": feature.cls,
                "z": 0,
                "height": 220,
                "type": feature.cls
            })
        for feature in wall.windows:
            if wall.isHorizontal:
                fromPosition = feature.fr.x-wall.min.x
                toPosition = feature.to.x-wall.min.x
            else:
                fromPosition = feature.fr.y-wall.min.y
                toPosition = feature.to.y-wall.min.y

            # print(feature)
            w["features"].append({
                "fromPosition": fromPosition*SCALE,
                "toPosition": toPosition*SCALE,
                "hinge": fromPosition*SCALE,
                "openLeft": False,
                "style": feature.cls,
                "z": 0,
                "height": 220,
                "type": feature.cls
            })
        w["features"] = sorted(w["features"],key=lambda k:k["fromPosition"])
        response["walls"].append(w)
    for item in plan.furniture:
        response["furniture"].append({
            "fromPosition":{
                "x": item.fr.x,
                "y": item.fr.y,
            },
            "toPosition":{
                "x": item.to.x,
                "y": item.to.y,
            },
            "item": item.obj,
            "z": idx*TARGET_CEILING_HEIGHT
        })
    
response["floors"] = {
    "fromPosition":{
        "x": (min[0])*SCALE,
        "y": (min[1])*SCALE,
    },
    "toPosition":{
        "x": (max[0])*SCALE,
        "y": (max[1])*SCALE,
    },
    "floors": len(floorplans),
    "height": TARGET_CEILING_HEIGHT
}

print(f"{n} walls found")
# print(response)

myclient = pymongo.MongoClient(f"mongodb://{CONFIG.getDB_HOST()}:{CONFIG.getDB_PORT()}/")
mydb = myclient[CONFIG.getDB_DATABASE()]
dbCollection = mydb["floorplans"]
json = jsonpickle.encode(response, unpicklable=False)
id = dbCollection.insert_one(jsonpickle.decode(json))
response["_id"] = str(id.inserted_id)
# print(response)
print(f"Floorplan ID= {str(id.inserted_id)}")


print(response_timer)
print(together_timer)