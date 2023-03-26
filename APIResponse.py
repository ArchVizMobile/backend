from typing import List

class Position:
    def __init__(self,x:int,y:int) -> None:
        self.x = x
        self.y = y
        pass

class Door:
    def __init__(self,fromPosition:int,toPosition:int,hinge:int,openLeft:bool,style:str) -> None:
        self.fromPosition = fromPosition
        self.toPosition = toPosition
        self.hinge = hinge
        self.openLeft = openLeft
        self.style = style
        pass

class Window:
    def __init__(self,fromPosition:int,toPosition:int,style:str) -> None:
        self.fromPosition = fromPosition
        self.toPosition = toPosition
        self.style = style
        pass

class Wall:
    def __init__(self,fromPosition:Position,toPosition:Position,isHorizontal:bool,isOuterWall:bool,doors:List[Door],windows:List[Window]) -> None:
        self.fromPosition = fromPosition
        self.toPosition = toPosition
        self.isHorizontal = isHorizontal
        self.isOuterWall = isOuterWall
        self.doors = doors
        self.windows = windows
        pass

class Junction:
    def __init__(self,success:bool,walls:None) -> None:
        self.success = success
        pass

class APIResponse:
    def __init__(self,success:bool,walls:List[Wall],junctions:List[Junction]) -> None:
        self.success = success
        self.walls = walls
        self.junctions = junctions
        pass