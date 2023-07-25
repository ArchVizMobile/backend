import glob
import os
import random
import re
import time
from typing import List, NamedTuple

from utils.hvh.parse import MinMaxValue, getDataByLine, getMinMaxValuesBySVG

from PIL import Image

def generateSvg(basefile:str):
    t = round(time.time())
    os.system(f'mkdir uploaded/{t} && pdf2svg "{basefile}" uploaded/{t}/%d.svg all')
    return t

class Color:
    def __init__(self,color:str):
        self.color = color

    def check(self,line:str):
        return re.search(r"fill:rgb\("+self.color+"\)",line)!=None

header_bar = Color("87.889099%,92.576599%,96.484375%")
outer_wall = Color("83.59375%,83.59375%,83.59375%")
inner_wall = Color("50%,50%,50%")
input_field = Color("96.875%,96.875%,96.875%")
table_heading = Color("88.28125%,88.28125%,88.28125%")
entry = Color("39.501953%,39.501953%,39.501953%")
footerHeightOffset = 10

def getHeaderBar(svgLines:List[str]):
    for line in svgLines:
        if header_bar.check(line):
            return getMinMaxValuesBySVG(getDataByLine(line))
    return None

def getFooter(svgLines:List[str]):
    found:List[MinMaxValue] = []
    for line in svgLines:
        if input_field.check(line) or table_heading.check(line):
            temp = getMinMaxValuesBySVG(getDataByLine(line))
            if temp!=None:
                found.append(temp)
        
    if len(found)==0:
        return None
    
    min = found[0]
    for item in found:
        if item.y.min < min.y.min:
            min = item

    return min

def getWalls(svgLines:List[str]):
    lines = []
    for line in svgLines:
        dat = getMinMaxValuesBySVG(getDataByLine(line))

        if re.search(r"fill:rgb(87.889099%,92.576599%,96.484375%);",line) != None:
            print("asd"+line)

        if re.search(r"fill:rgb\(50%,50%,50%\);",line) != None or \
            re.search(r"fill:rgb\(83.59375%,83.59375%,83.59375%\)",line) != None or \
            re.search(r"fill:rgb\(67.1875%,67.1875%,67.1875%\)",line) != None or\
            re.search(r"fill:rgb\(39.501953%,39.501953%,39.501953%\)",line) != None:
            lines.append(dat)
    return lines

class DeadZonedLines:
    def __init__(self,data:MinMaxValue,raw:str,isDead:bool) -> None:
        self.data = data
        self.raw = raw
        self.isDead = isDead

def getMinMaxValuesBySVGFromXAndY(line:str):
    # dat = MinMaxValue([0,0])
    x = -1
    y = -1
    for l in line.split(" "):
        if l.startswith("x="):
            x = int(l.split("\"")[1].split(".")[0])
        if l.startswith("y="):
            y = int(l.split("\"")[1].split(".")[0])
    if x!=-1 and y!=-1:
        return MinMaxValue([x,y],[x,y])
    return None
    
def removeDeadZones(svg:List[str],header:MinMaxValue,height:int=0,footer:MinMaxValue=None):
    lines:List[DeadZonedLines] = []
    for line in svg:
        dat = getMinMaxValuesBySVG(getDataByLine(line))
        # lines.append(DeadZonedLines(dat,line))
        if dat==None:
            dat = getMinMaxValuesBySVGFromXAndY(line)

        if dat==None:
            lines.append(DeadZonedLines(dat,line,False))

        if dat!=None and dat.y.min >= header.y.max:
            lines.append(DeadZonedLines(dat,line,True))
            # if footer!=None:
                # if dat.y.max <= footer.y.min:
                    # lines.append(DeadZonedLines(dat,line))
            # else:
                # if dat.y.max <= height - footerHeightOffset:
                    # lines.append(DeadZonedLines(dat,line))
    return lines

def analyzeHvhSvg(t):
    pages = {}
    min = [999999999,999999999]
    max = [0,0]


    for idx,file in enumerate(glob.glob(f"uploaded/{t}/*.svg")):
        page = int(file.split(".")[0].split("/")[-1:][0])
        tmin = [999999999,999999999]
        tmax = [0,0]
        minDepth = 999999999999
        lines = []
        svg = []
        with open(file) as handler:
            svg = handler.read().split("\n")
            decl = svg[1].split(" ")
            height = 842
            for item in decl:
                if item.startswith("height"):
                    height = int(item.split("\"")[1].removesuffix("pt"))

            header = getHeaderBar(svg)
            footer = getFooter(svg)
            if header != None:
                os.system(f"convert -density 1000 {file} uploaded/{t}/{idx+1}.png")
                # with Image.open(f"uploaded/{t}/{idx+1}.png") as im:
                    # im.show()
                # lines = removeDeadZones(svg,header,height,footer)
                # # print(f"header = {header} footer={footer} height={height} lines={lines}")
                # f = open(f"{idx+1}.temp.svg", "w")
                # # f.write('<?xml version="1.0" encoding="UTF-8"?>')
                # # f.write('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="595pt" height="842pt" viewBox="0 0 595 842" version="1.1">')

                # for line in lines:
                #     f.write(line.raw)
                # # f.write("</svg>")
                # f.close()
                # print(f"Wrote {idx+1}.temp.svg")

                # lines = getWalls(svg,header,footer,height)
                # print(lines)

        # if len(lines) > 10:
        #     for item in lines:
        #         if item[0]<tmin:
        #             tmin[0] = item[0][0]
        #             tmin[1] = item[0][1]
        #         if item[0]>tmax:
        #             tmax[0] = item[0][0]
        #             tmax[1] = item[0][1]

        #     # print(tmin)
        #     for idx,item in enumerate(lines):
        #         lines[idx][0][0] = (lines[idx][0][0]) # - tmin[0])
        #         lines[idx][0][1] = (lines[idx][0][1]) # - tmin[1])

        #         lines[idx][1][0] = (lines[idx][1][0]) # - tmin[0])
        #         lines[idx][1][1] = (lines[idx][1][1]) # - tmin[1])
        #         isHorizontal = lines[idx][1][0]-lines[idx][0][0] > lines[idx][1][1]-lines[idx][0][1]
                
        #         depth = lines[idx][1][0]-lines[idx][0][0] if not isHorizontal else lines[idx][1][1]-lines[idx][0][1]
        #         if depth < minDepth and depth >= 1:
        #             minDepth = depth
        #     if tmax[1]-tmin[1] < 0 or tmax[0]-tmin[0] < 0:
        #         pages[page] = {
        #             "type": "unknown",
        #             "page": page,
        #             "data": svg
        #         }
        #     else:
        #         pages[page] = {
        #             "min": tmin,
        #             "max": tmax,
        #             "width": tmax[0]-tmin[0],
        #             "height": tmax[1]-tmin[1],
        #             "lines": lines,
        #             "type": "floorplan",
        #             "page": page
        #         }
        # else:
        #     pages[page] = {
        #         "type": "unknown",
        #         "page": page,
        #         "data": svg
        #     }
        # if tmin[0]<min[0]: min[0] = tmin[0]
        # if tmin[1]<min[1]: min[1] = tmin[1]
        # if tmax[0]>max[0]: max[0] = tmax[0]
        # if tmax[1]>max[1]: max[1] = tmax[1]
    return pages,min,max

def GET(self,dbCollection,search):

    files = glob.glob("uploaded/*.pdf")
    basefile = files[random.randint(0,len(files)-1)]
    basefile = "uploaded/Calvus 620.pdf"


    # TODO: Handle file upload?
    t = generateSvg(basefile)


    pages,min,max = analyzeHvhSvg(t)
    return [pages[page] for page in pages if pages[page]["type"]=="floorplan" ]
    
    if len(pages)<=0:
        return {
            "_id": "-1",
            "info": {
                "basefile":basefile,
                "number_of_floorplans_in_file":len(pages),
                "chosen_plan":-1
            },
            "success": False,
            "name": "",
            "walls": [],
            "junctions": [],
            "rooms": [],
            "scale": -1
        }

    chosen_plan = random.randint(0,len(pages)-1)
    # chosen_plan = len(pages)-1
    print(f"@{basefile}: no {chosen_plan} of {len(pages)}")

    data = []
    # [chosen_plan]
    for all in pages:
        d = []
        for wall in all:
            isHorizontal = wall[1][0]-wall[0][0] > wall[1][1]-wall[0][1]
            
            depth = wall[1][0]-wall[0][0] if not isHorizontal else wall[1][1]-wall[0][1]

            d.append({
                "fromPosition": {
                    "x": wall[0][0],
                    "y": wall[0][1]
                },
                "toPosition": {
                    "x": wall[1][0],
                    "y": wall[1][1]
                },
                "isHorizontal": isHorizontal,
                "isOuterWall": True,
                "features": [],
                "depth": depth,
                "height": 391
            })
        data.append(d)

    os.system(f"rm -rf uploaded/{t}")
    
    return {
        "_id": "-1",
        "info": {
            "basefile":basefile,
            "number_of_floorplans_in_file":len(pages),
            "chosen_plan":chosen_plan
        },
        "success": True,
        "name": "Heinz von Heiden "+basefile.split("/")[1].split(".")[0],
        "walls": data[chosen_plan],
        "all_walls": data,
        "junctions": [],
        "rooms": [],
        "scale": scale
    }

if __name__=="__main__":
    GET()
