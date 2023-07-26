import glob
import os
import re
import time
from typing import List

from routes.floorplan.hvh.parse.get import Color, getFooter, getHeaderBar
from utils.hvh.parse import MinMaxValue, getAttributeDataFromSvg, getDataByLine, getWallInformationBySVG

def createSVGs():
    for idx,file in enumerate(glob.glob(f"uploaded/*.pdf")):
        baseName = file.split(".")[0].split("/")[1]
        os.system(f'mkdir "uploaded/{baseName}" && pdf2svg "{file}" "uploaded/{baseName}/%d.svg" all')
        for svgidx,svg in enumerate(glob.glob(f"uploaded/{baseName}/*.svg")):
            print(svg)
            os.system(f"convert -density 1000 \"{svg}\" \"uploaded/{baseName}/{svgidx+1}.png\"")

header_bar = Color("87.889099%,92.576599%,96.484375%")
outer_wall = Color("83.59375%,83.59375%,83.59375%")
inner_wall = Color("50%,50%,50%")
input_field = Color("96.875%,96.875%,96.875%")
table_heading = Color("88.28125%,88.28125%,88.28125%")
entry = Color("39.501953%,39.501953%,39.501953%")
footerHeightOffset = 10


def analyzeSVG(baseName:str):
    linez = []

    cache:List[MinMaxValue] = []

    with open(baseName) as handler:
        newBaseName = baseName.replace(".svg",".corrected.svg")
        correctedSvg = open(newBaseName, "w")

        svg = handler.read().split("\n")

        header = getHeaderBar(svg)

        # Get SVG Height & check max available height
        decl = svg[1].split(" ")
        height = 842
        for item in decl:
            if item.startswith("height"):
                height = int(item.split("\"")[1].removesuffix("pt"))
        maxHeight = height - 30
        footer = getFooter(svg)
        if footer!=None:
            maxHeight = footer.y.min


        if header != None:
            for line in svg:
                data = getWallInformationBySVG(getDataByLine(line),line)
                if data!=None and data.y.min >= header.y.max and data.y.max <= maxHeight and ( inner_wall.check(line) or  outer_wall.check(line)):
                    linez.append([line,data])
                    cache.append(data)

        correctedSvg.write(svg[0]+"\n")
        correctedSvg.write(svg[1]+"\n")

        for line,data in linez:
            if line.startswith("<path"):
                style = line.split("style=\"")[1].split("\"")[0]
                d = line.split("d=\"")[1].split("\"")[0]
                line = line.replace(d,data.getCorrected())
                try:
                    transform = line.split("transform=\"")[1].split("\"")[0]
                    line = line.replace(transform,"")
                except:
                    pass
                correctedSvg.write(line+"\n")
            else:
                correctedSvg.write(line+"\n")
        correctedSvg.write(svg[len(svg)-2]+"\n")
        correctedSvg.close()
    return linez

# baseName = "uploaded/Calvus 620/4.svg"
# linez = analyzeSVG(baseName)
# print(linez)

IMAGE_SCALE_FACTOR = 10

def generateSVGs(file:str):
    baseName = file.split(".")[0].split("/")[1]
    print(f"[{baseName}] Parsing SVGs from PDF")
    os.system(f'mkdir "uploaded/{baseName}" && pdf2svg "{file}" "uploaded/{baseName}/%d.svg" all')
    svgs = glob.glob(f"uploaded/{baseName}/*.svg")
    print(f"[{baseName}] Creating Images from SVGs")
    for svgidx,svg in enumerate(svgs):
        print(f"[{baseName}] {svgidx+1}/{len(svgs)}")
        os.system(f"convert -density {100*IMAGE_SCALE_FACTOR} \"{svg}\" \"uploaded/{baseName}/{svgidx+1}.png\"")
    return svgs,[f.replace(".svg",".png") for f in svgs]

# svgs,pngs = generateSVGs("uploaded/Calvus 631.pdf")
svgs = ['uploaded/Calvus 631/1.svg', 'uploaded/Calvus 631/2.svg', 'uploaded/Calvus 631/3.svg', 'uploaded/Calvus 631/4.svg', 'uploaded/Calvus 631/5.svg']
pngs = ['uploaded/Calvus 631/1.png', 'uploaded/Calvus 631/2.png', 'uploaded/Calvus 631/3.png', 'uploaded/Calvus 631/4.png', 'uploaded/Calvus 631/5.png']
# print(svgs)
# print(pngs)

floorplans = []

for svg in svgs:
    with open(svg) as file_handler:
        lines = file_handler.read().split("\n")
        # print(lines)
        header = getHeaderBar(lines)

        height = 842
        try:
            height = float(getAttributeDataFromSvg(lines[1],"height").removesuffix("pt"))
        except:
            pass


        maxHeight = height - 30
        footer = getFooter(lines)
        if footer!=None:
            maxHeight = footer.y.min

        print(maxHeight)
        print(header.y.max)

        # for line in lines:
        #     data = getWallInformationBySVG(line)
        #     if data!=None and data.min.y >= header.y.max and data.max.y <= maxHeight and ( inner_wall.check(line) or  outer_wall.check(line)):
        #         floorplans.append({
        #             "lines":lines
        #         })
