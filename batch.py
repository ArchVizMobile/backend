import glob
import os
import time

from routes.floorplan.hvh.parse.get import getFooter, getHeaderBar
from utils.hvh.parse import getDataByLine, getMinMaxValuesBySVG

def createSVGs():
    for idx,file in enumerate(glob.glob(f"uploaded/*.pdf")):
        baseName = file.split(".")[0].split("/")[1]
        os.system(f'mkdir "uploaded/{baseName}" && pdf2svg "{file}" "uploaded/{baseName}/%d.svg" all')
        for svgidx,svg in enumerate(glob.glob(f"uploaded/{baseName}/*.svg")):
            print(svg)
            os.system(f"convert -density 1000 \"{svg}\" \"uploaded/{baseName}/{svgidx+1}.png\"")

with open("uploaded/Calvus 631/4.svg") as handler:
    svg = handler.read().split("\n")
    decl = svg[1].split(" ")
    height = 842
    for item in decl:
        if item.startswith("height"):
            height = int(item.split("\"")[1].removesuffix("pt"))

    maxHeight = height - 30

    header = getHeaderBar(svg)
    footer = getFooter(svg)
    if footer!=None:
        maxHeight = footer.y.min
    # print(header)
    # print(footer)
    print('<?xml version="1.0" encoding="UTF-8"?>')
    print('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="595pt" height="842pt" viewBox="0 0 595 842" version="1.1">')

    if header != None:
        for line in svg:
            data = getMinMaxValuesBySVG(getDataByLine(line))
            if data!=None and data.y.min >= header.y.max and data.y.max <= maxHeight:
                print(line)
    print('</svg>')
