from utils.hvh.parse import getColorByLine, getDataByLine, getMinMaxValuesBySVG


def filter(f):
    file = f
    with open(file) as handler:
        svg = handler.read().split("\n")
        for line in svg:
            try:
                min, max = getMinMaxValuesBySVG(getDataByLine(line))
                
                if (min[1] > 85 and max[1] < 159):
                    print(line)
                elif (min[1] < 0):
                    print(line)
            except:
                pass
filter ("Alto 530.svg")