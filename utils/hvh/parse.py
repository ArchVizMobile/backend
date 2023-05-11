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
                if temp < min:
                    min[0] = temp[0]
                    min[1] = temp[1]
                
                if temp > max:
                    max[0] = temp[0]
                    max[1] = temp[1]

    return min,max
