import json
import logging
from dataclasses import dataclass
from ultralytics import YOLO

from common.ModelTrainer import ModelData


@dataclass
class StairData:
    name: str


@dataclass
class StairDetectionRequest:
    image: str


@dataclass
class StairDetectionResponse:
    response: int


class StairService:
    def __init__(self, model_data: ModelData):
        self.model = YOLO(model_data.path)

    def detect(self, request: StairDetectionRequest) -> StairDetectionResponse:
        results = self.model.predict(request.image, save=True)

        detected_objects = []
        for res in results:
            predictions = res.boxes.data.tolist()
            class_names = res.names

            for pred in predictions:
                xmin, ymin, xmax, ymax = pred[:4]
                detected_class = class_names[int(pred[5])]
                obj = {
                    'xmin': int(xmin),
                    'ymin': int(ymin),
                    'xmax': int(xmax),
                    'ymax': int(ymax),
                    'class': detected_class
                }
                detected_objects.append(obj)

        with open('detected_objects.json', 'w') as f:
            json.dump(detected_objects, f)
        return StairDetectionResponse(len(detected_objects))
