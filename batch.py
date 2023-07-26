import glob
import os
import time
from typing import List
from PIL import Image, ImageChops

from routes.floorplan.hvh.parse.get import Color, getFooter, getHeaderBar
from utils.hvh.parse import MinMaxValue, Point, Wall, getAttributeDataFromSvg, getDataByLine, getWallInformationBySVG

header_bar = Color("87.889099%,92.576599%,96.484375%")
outer_wall = Color("83.59375%,83.59375%,83.59375%")
inner_wall = Color("50%,50%,50%")
input_field = Color("96.875%,96.875%,96.875%")
table_heading = Color("88.28125%,88.28125%,88.28125%")
entry = Color("39.501953%,39.501953%,39.501953%")
footerHeightOffset = 10

IMAGE_SCALE_FACTOR = 4

class Floorplan:
    def __init__(self,
            image:str,
            svg:List[str],
            bbox:tuple[int, int, int, int],
            header:MinMaxValue,
            height:float,
            maxHeight:int) -> None:
        self.image = image
        self.svg = svg
        self.bbox = bbox
        self.header = header
        self.height = height
        self.maxHeight = maxHeight
        self.walls:List[Wall] = []

        for line in svg:
            wall = getWallInformationBySVG(line)
            if wall!=None:
                self.walls.append(wall)

    def __repr__(self) -> str:
        return f"Floorplan({self.image})"

def generateSVGs(file:str):
    baseName = file.split(".")[0].split("/")[1]
    print(f"[{baseName}] Parsing SVGs from PDF")
    os.system(f'mkdir "uploaded/{baseName}"')
    os.system(f'pdf2svg\dist-64bits\pdf2svg.exe "{file}" "uploaded/{baseName}/%d.svg" all')
    svgs = glob.glob(f"uploaded/{baseName}/*.svg")
    print(f"[{baseName}] Creating Images from SVGs")
    for svgidx,svg in enumerate(svgs):
        print(f"[{baseName}] {svgidx+1}/{len(svgs)}")
        cmd = f'ImageMagick\convert.exe -density {100*IMAGE_SCALE_FACTOR} "{svg}" "uploaded/{baseName}/{svgidx+1}.png"'
        print(cmd)
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
                floorplans.append(Floorplan(newFile,lines,bbox,header,height,maxHeight))

    return floorplans,svgs,pngs

class Timer:
    def __init__(self) -> None:
        self.start = time.time()
        pass

    def __str__(self):
        end = time.time()
        return (f"Took ~{round(end-self.start)}s")

generate_timer = Timer()
floorplans,svgs,pngs = GenerateFloorplans("uploaded/Calvus 631.pdf")
print(generate_timer)

for plan in floorplans:
    print(plan.walls)
