from utils.hvh.parse import getDataByLine, getMinMaxValuesBySVG
from routes.floorplan.hvh.parse.get import Color, getFooter, getHeaderBar

tree_color  = Color("67.1875%,67.1875%,67.1875%")
glass_color1 = Color("82.8125%,88.28125%,92.1875%")


base_color = Color("71.875%,71.875%,71.875%")

step_color1 = Color("64.0625%,64.0625%,64.0625%")
step_color2 = Color("57.03125%,57.03125%,57.03125%")

shadow_color = Color("83.59375%,83.59375%,83.59375%")

roof_color1 = Color("69.921875%,67.1875%,70.3125%")
roof_color2 = Color("63.671875%,60.9375%,64.0625%")
 
pump_color1 = Color("75%,75%,75%")
pump_color2 = Color("66.796875%,66.796875%,66.796875%")

hinges_color = Color("90.234375%,90.234375%,90.234375%")

frame_color1 = Color("93.359375%,93.359375%,93.359375%")
frame_color2 = Color("83.201599%,83.201599%,83.201599%")
frame_color3 = Color("75.389099%,77.734375%,81.25%")     # eigentlich Fensterbrett
frame_color4 = Color("66.796875%,69.139099%,72.264099%") # eigentlich Fensterbrett

drain_color = [Color("78.125%,84.375%,82.421875%"), Color("79.296875%,85.546875%,83.59375%"), Color("82.03125%,88.671875%,86.71875%"), Color("85.15625%,91.796875%,89.451599%"), Color("86.71875%,93.75%,91.40625%"), Color("83.201599%,89.84375%,87.889099%"), Color("87.889099%,94.921875%,92.576599%"), Color("85.546875%,92.576599%,90.234375%"), Color("87.109375%,94.139099%,91.796875%"), Color("84.764099%,91.40625%,89.451599%"), Color("82.421875%,89.0625%,87.109375%"), Color("89.84375%,96.875%,94.53125%"), Color("88.28125%,95.3125%,92.96875%"), Color("80.076599%,86.326599%,84.375%"), Color("82.8125%,89.451599%,87.5%"), Color("85.15625%,92.1875%,89.84375%"), Color("88.671875%,95.701599%,93.359375%"), Color("78.514099%,84.764099%,82.8125%"), Color("89.0625%,96.09375%,93.75%"), Color("80.859375%,87.5%,85.546875%"), Color("87.5%,94.53125%,92.1875%"), Color("80.46875%,87.109375%,85.15625%"), Color("81.25%,87.889099%,85.9375%"), Color("83.59375%,90.234375%,88.28125%"), Color("86.326599%,93.359375%,91.014099%"), Color("80.46875%,86.71875%,84.764099%"), Color("73.046875%,73.046875%,73.046875%"), Color("90.234375%,97.264099%,94.921875%"), Color("90.234375%,97.65625%,95.3125%"), Color("91.40625%,98.826599%,96.484375%"), Color("85.9375%,92.96875%,90.625%"), Color("83.984375%,90.625%,88.671875%"), Color("78.90625%,85.15625%,83.201599%"), Color("")]

vent_color = Color("72.65625%,72.65625%,72.65625%")

contur_color1 = Color("95.3125%,95.3125%,95.3125%")
contur_color2 = Color("84.764099%,84.764099%,84.764099%")

black = Color("0%,0%,0%")
white = Color("100%,100%,100%")

groundLevel = 154.078125

def filterView(f):
    file = f
    with open(file) as handler:
        svg = handler.read().split("\n")
        header = getHeaderBar(svg)
        maxHeight = 159
        print('<?xml version="1.0" encoding="UTF-8"?>')
        print('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="595pt" height="842pt" viewBox="0 0 595 842" version="1.1">')
        for line in svg:
            try:             
                data = getMinMaxValuesBySVG(getDataByLine(line))
                if data != None and data.y.min >= header.y.max and data.y.max <= maxHeight and not tree_color.check(line) and not (data.x.max - data.x.min) > 400:    
                    print(line)
            except:
                pass
        print('</svg>')

# filterView ("Alto 530.svg")

def findGlass(f):
    file = f
    with open(file) as handler:
        svg = handler.read().split("\n")
        print('<?xml version="1.0" encoding="UTF-8"?>')
        print('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="595pt" height="842pt" viewBox="0 0 595 842" version="1.1">')
        for line in svg:
            try:             
                if glass_color1.check(line):
                    print(line)
            except:
                pass
        print('</svg>')

# findGlass("Alto1.svg")

def findWindow(f):
    file = f
    # findGlass("file")

    with open(file) as handler:
        svg = handler.read().split("\n")
        print('<?xml version="1.0" encoding="UTF-8"?>')
        print('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="595pt" height="842pt" viewBox="0 0 595 842" version="1.1">')
        for line in svg:
            try:             
                data = getMinMaxValuesBySVG(getDataByLine(line))
                if glass_color1.check(line) and (groundLevel - data.y.max) > 5 and (data.x.max - data.x.min) > 2:
                    try: 
                        for line1 in svg:           
                            data1 = getMinMaxValuesBySVG(getDataByLine(line1))
                            if data.y.min >= data1.y.max and (data.x.max - data.y.min) < (data1.x.max - data1.y.min) and not glass_color1.check(line):
                                print(line)   
                    except:
                        pass 
                    print(line)    
            except:
                pass
        print('</svg>')

# findWindow("Alto 530.svg")

def findDoor(f):
    file = f
    with open(file) as handler:
        svg = handler.read().split("\n")
        header = getHeaderBar(svg)
        maxHeight = 159
        print('<?xml version="1.0" encoding="UTF-8"?>')
        print('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="595pt" height="842pt" viewBox="0 0 595 842" version="1.1">')
        for line in svg:
            try:             
                data = getMinMaxValuesBySVG(getDataByLine(line))
                if data != None and data.y.min >= header.y.max and data.y.max <= maxHeight and not tree_color.check(line) and not (data.x.max - data.x.min) > 400:    
                    if groundLevel -18 < data.y.min and groundLevel - 13 > data.y.min and (data.y.max - data.y.min) > 13:    
                        print(line)
            except:
                pass
        print('</svg>')

# findDoor("Alto 530.svg")

def findBase(f):
    file = f
    with open(file) as handler:
        svg = handler.read().split("\n")
        header = getHeaderBar(svg)
        maxHeight = 159
        print('<?xml version="1.0" encoding="UTF-8"?>')
        print('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="595pt" height="842pt" viewBox="0 0 595 842" version="1.1">')
        for line in svg:
            try:             
                data = getMinMaxValuesBySVG(getDataByLine(line))
                if data != None and data.y.min >= header.y.max and data.y.max <= maxHeight and not tree_color.check(line) and not (data.x.max - data.x.min) > 400:    
                    if groundLevel - 4 < data.y.min and base_color.check(line):    
                        print(line)
            except:
                pass
        print('</svg>')

# findBase("Alto 530.svg")

def findDoorstep(f):
    file = f
    with open(file) as handler:
        svg = handler.read().split("\n")
        header = getHeaderBar(svg)
        maxHeight = 159
        print('<?xml version="1.0" encoding="UTF-8"?>')
        print('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="595pt" height="842pt" viewBox="0 0 595 842" version="1.1">')
        for line in svg:
            try:             
                data = getMinMaxValuesBySVG(getDataByLine(line))
                if data != None and data.y.min >= header.y.max and data.y.max <= maxHeight and not tree_color.check(line) and not (data.x.max - data.x.min) > 400:    
                    if groundLevel - 4 < data.y.min and (step_color1.check(line) or step_color2.check(line)):    
                        print(line)
            except:
                pass
        print('</svg>')

# findDoorstep("Alto 530.svg")

def findDrain(f):
    file = f
    with open(file) as handler:
        svg = handler.read().split("\n")
        header = getHeaderBar(svg)
        maxHeight = 159
        print('<?xml version="1.0" encoding="UTF-8"?>')
        print('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="595pt" height="842pt" viewBox="0 0 595 842" version="1.1">')
        for line in svg:
            try:             
                data = getMinMaxValuesBySVG(getDataByLine(line))
                if data != None and data.y.min >= header.y.max and data.y.max <= maxHeight and not tree_color.check(line) and not (data.x.max - data.x.min) > 400:    
                    for color in drain_color:
                            if color.check(line):
                                print(line)
            except:
                pass
        print('</svg>')

# findDrain("Alto 530.svg")

def findRoof(f):
    file = f
    with open(file) as handler:
        svg = handler.read().split("\n")
        header = getHeaderBar(svg)
        maxHeight = 159
        n = 0
        max_y = 0
        min_y = 0
        x = 0
        print('<?xml version="1.0" encoding="UTF-8"?>')
        print('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="595pt" height="842pt" viewBox="0 0 595 842" version="1.1">')
        for line in svg:
            try:             
                data = getMinMaxValuesBySVG(getDataByLine(line))
                if data != None and data.y.min >= header.y.max and data.y.max <= maxHeight and not tree_color.check(line) and not (data.x.max - data.x.min) > 400:    
                    if roof_color1.check(line):
                        if n == 0:
                            x = data.x.max - data.x.min
                            max_y = data.y.max
                            min_y = data.y.min
                            n = 1 
                        print(line)
            except:
                pass
        
        for line in svg:
            try:             
                data = getMinMaxValuesBySVG(getDataByLine(line))
                if data != None and data.y.min >= header.y.max and data.y.max <= maxHeight and not tree_color.check(line) and not (data.x.max - data.x.min) > 400:    
                    if (data.y.max <= max_y and data.y.min >= min_y and data.y.max >= max_y - 8 and data.y.min <= min_y + 8) or (data.y.max <= max_y and data.y.min >= min_y and x - 1 <= data.x.max - data.x.min):
                        print(line)
            except:
                pass
        
        print('</svg>')

# findRoof("Alto 530.svg") 

def filterColor(f):
    file = open(Altofind.svg, "w")

    with open(f) as handler:
        svg = handler.read().split("\n")
        header = getHeaderBar(svg)
        maxHeight = 159
        file.write(svg[0]+"\n")
        file.write(svg[1]+"\n")
        for line in svg:
            try:             
                data = getMinMaxValuesBySVG(getDataByLine(line))
                if data != None and data.y.min >= header.y.max and data.y.max <= maxHeight and not tree_color.check(line) and not (data.x.max - data.x.min) > 400:
                    if not white.check(line) and not hinges_color.check(line) and not vent_color.check(line) and not contur_color2.check(line) and not contur_color1.check(line)  and not frame_color4.check(line) and not frame_color3.check(line) and not frame_color2.check(line) and not frame_color1.check(line) and not pump_color2.check(line) and not pump_color1.check(line) and not step_color2.check(line) and not roof_color2.check(line) and not roof_color1.check(line) and not black.check(line) and not base_color.check(line) and not glass_color1.check(line) and not step_color1.check(line) and not shadow_color.check(line):    
                        file.write(line + "\n")
            except:
                pass
        file.write(svg[len(svg)-2] + "\n")
    file.close()

# filterColor("Alto 530.svg")

