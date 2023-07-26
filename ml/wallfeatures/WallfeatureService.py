import dataclasses
import json
import logging
from dataclasses import dataclass
from enum import StrEnum, auto
from typing import List

from ultralytics import YOLO

from ..common.ModelTrainer import ModelData
from ..common.YoloResponse import YoloResponse
from ..common.DataClassJsonEncoder import DataClassJsonEncoder


class Classes(StrEnum):
    WINDOW = "window"
    DOOR = "door"
    DOUBLEDOOR = "doubleDoor"
    ROOFWALL = "roofWall"
    ROOFWINDOW = "roofWindow"

@dataclass
class WallFeatureDetectionRequest:
    image: str


@dataclass
class WallFeatureDetectionResponse:
    window: List[YoloResponse] = None
    door: List[YoloResponse] = None
    doubleDoor: List[YoloResponse] = None
    roofWall: List[YoloResponse] = None
    roofWindow: List[YoloResponse] = None


class WallFeatureService:
    def __init__(self, model_data: ModelData):
        self.model = YOLO(model_data.path)
        self.model_data = model_data

    def detect(self, request: str) -> WallFeatureDetectionResponse:
        results = self.model.predict(request, save=False, conf=0.5)

        response = WallFeatureDetectionResponse()
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
                    case Classes.WINDOW:
                        if response.window is None:
                            response.window = []
                        response.window.append(obj)
                    case Classes.DOOR:
                        if response.door is None:
                            response.door = []
                        response.door.append(obj)
                    case Classes.DOUBLEDOOR:
                        if response.doubleDoor is None:
                            response.doubleDoor = []
                        response.doubleDoor.append(obj)
                    case Classes.ROOFWALL:
                        if response.roofWall is None:
                            response.roofWall = []
                        response.roofWall.append(obj)
                    case Classes.ROOFWINDOW:
                        if response.roofWindow is None:
                            response.roofWindow = []
                        response.roofWindow.append(obj)

        # with open('detected_objects_wallfeatures.json', 'w') as f:
        #     json.dump(response, f, cls=DataClassJsonEncoder)
        return response
