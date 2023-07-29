import dataclasses
import json
import logging
import enum
from dataclasses import dataclass
from enum import StrEnum, auto
from typing import List

from ultralytics import YOLO

from ..common.ModelTrainer import ModelData
from ..common.YoloResponse import YoloResponse
from ..common.DataClassJsonEncoder import DataClassJsonEncoder

#Keine Ahnung bekomme das mit dem Enum nicht hin. Immer ein  File "D:\Anaconda\envs\data\Lib\enum.py", line 789, in __getattr__    raise AttributeError(name) from None AttributeError: armchair
#im match mach ich das jetzt einfach mit strings das scheint zu funktionieren.
class FurnitureClasses(StrEnum):
    ARMCHAIR = "armchair"
    BATHTUB = "bathtub"
    BED = "bed"
    COUCH = "couch"
    DESK = "desk"
    DINING_TABLE_4_CHAIRS = "dining_table_4_chairs"
    DINING_TABLE_6_CHAIRS = "dining_table_6_chairs"
    KITCHENETTE = "kitchenette"
    LOWBOARDTV = "lowboardTV"
    MASTERBED = "masterbed"
    SHELF = "shelf"
    SHOWER = "shower"
    SINK = "sink"
    TABLE = "table"
    WC = "wc"



@dataclass
class FurnitureDetectionRequest:
    image: str


@dataclass
class FurnitureDetectionResponse:
    armchair: List[YoloResponse] = None
    bathtub: List[YoloResponse] = None
    bed: List[YoloResponse] = None
    couch: List[YoloResponse] = None
    desk: List[YoloResponse] = None
    dining_table_4_chairs: List[YoloResponse] = None
    dining_table_6_chairs: List[YoloResponse] = None
    kitchenette: List[YoloResponse] = None
    lowboardTV: List[YoloResponse] = None
    masterbed: List[YoloResponse] = None
    shelf: List[YoloResponse] = None
    shower: List[YoloResponse] = None
    sink: List[YoloResponse] = None
    table: List[YoloResponse] = None
    wc: List[YoloResponse] = None

class FurnitureService:
    def __init__(self, model_data: ModelData):
        self.model = YOLO(model_data.path)
        self.model_data = model_data

    def detect(self, request: str) -> FurnitureDetectionResponse:
        results = self.model.predict(request, save=False,name="../../"+request.replace(".png",".furniture"),verbose=False)

        response = FurnitureDetectionResponse()
        for res in results:
            predictions = res.boxes.data.tolist()
            class_names = res.names

            for pred in predictions:
                xmin, ymin, xmax, ymax = pred[:4]
                detected_class = class_names[int(pred[5])]
                obj = YoloResponse(
                    xmin=int(xmin),
                    ymin=int(ymin),
                    xmax=int(xmax),
                    ymax=int(ymax),
                    object=detected_class
                )
                
                match detected_class:
                    case "armchair":
                        if response.armchair is None:
                            response.armchair = []
                        response.armchair.append(obj)
                    case "bathtub":
                        if response.bathtub is None:
                            response.bathtub = []
                        response.bathtub.append(obj)
                    case "bed":
                        if response.bed is None:
                            response.bed = []
                        response.bed.append(obj)
                    case "couch":
                        if response.couch is None:
                            response.couch = []
                        response.couch.append(obj)
                    case "desk":
                        if response.desk is None:
                            response.desk = []
                        response.desk.append(obj)
                    case "dining table 4 chairs":
                        if response.dining_table_4_chairs is None:
                            response.dining_table_4_chairs = []
                        response.dining_table_4_chairs.append(obj)
                    case "dining table 6 chairs":
                        if response.dining_table_6_chairs is None:
                            response.dining_table_6_chairs = []
                        response.dining_table_6_chairs.append(obj)
                    case "kitchenette":
                        if response.kitchenette is None:
                            response.kitchenette = []
                        response.kitchenette.append(obj)
                    case "lowboardTV":
                        if response.lowboardTV is None:
                            response.lowboardTV = []
                        response.lowboardTV.append(obj)
                    case "masterbed":
                        if response.masterbed is None:
                            response.masterbed = []
                        response.masterbed.append(obj)
                    case "shelf":
                        if response.shelf is None:
                            response.shelf = []
                        response.shelf.append(obj)
                    case "shower":
                        if response.shower is None:
                            response.shower = []
                        response.shower.append(obj)
                    case "sink":
                        if response.sink is None:
                            response.sink = []
                        response.sink.append(obj)
                    case "table":
                        if response.table is None:
                            response.table = []
                        response.table.append(obj)
                    case "wc":
                        if response.wc is None:
                            response.wc = []
                        response.wc.append(obj)

        # with open('detected_objects_Furniture.json', 'w') as f:
        #     json.dump(response, f, cls=DataClassJsonEncoder)
        return response
