import dataclasses
import json
import logging
from dataclasses import dataclass
from enum import StrEnum, auto

from ultralytics import YOLO

from ..common.ModelTrainer import ModelData
from ..common.YoloResponse import YoloResponse
from ..common.DataClassJsonEncoder import DataClassJsonEncoder


class Classes(StrEnum):
    STAIRS = auto()
    ENTRY = auto()
    ARROW = auto()


@dataclass
class StairDetectionRequest:
    image: str


@dataclass
class StairDetectionResponse:
    stair: YoloResponse = None
    entry: YoloResponse = None
    arrow: YoloResponse = None


class StairService:
    def __init__(self, model_data: ModelData):
        self.model = YOLO(model_data.path)
        self.model_data = model_data

    def detect(self, request: str) -> StairDetectionResponse:
        results = self.model.predict(request, save=True, conf=0.5)

        response = StairDetectionResponse()
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
                    case Classes.STAIRS:
                        response.stair = obj
                    case Classes.ENTRY:
                        response.entry = obj
                    case Classes.ARROW:
                        response.arrow = obj

        with open('detected_objects_stairs.json', 'w') as f:
            json.dump(response, f, cls=DataClassJsonEncoder)
        return response
