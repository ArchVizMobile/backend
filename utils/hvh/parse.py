import math


def getMinMaxValuesBySVG(d):
    da = d.split(" ")

    min = [ 9999999999999999999999, 9999999999999999999999]
    max = [-9999999999999999999999,-9999999999999999999999]

    temp = [0,0]

    i = 0

    for item in da:
        if not item=="M" and not item=="L" and not item=="Z" and not item=="":
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

    return min,max

def getDataByLine(line):
    return line.split(" d=\"")[1].split("\"")[0]

if __name__=="__main__":
    line = '<path style=" stroke:none;fill-rule:nonzero;fill:rgb(39.501953%,39.501953%,39.501953%);fill-opacity:1;" d="M 465.601562 391.917969 L 462.238281 400.320312 L 465.601562 408.960938 L 465.601562 391.917969 "/>'
    print(line)
    data = getDataByLine(line)
    print(data)
    coords = getMinMaxValuesBySVG(data)
    print(coords)