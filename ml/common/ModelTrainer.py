import logging
import os
import shutil

from dataclasses import dataclass
from ultralytics import YOLO
from enum import StrEnum, auto


class Models(StrEnum):
    STAIRS = auto()


@dataclass
class ModelData:
    model: Models
    path: str


class ModelTrainer:
    def __init__(self):
        self.base_model = YOLO("yolov8n.pt")
        self.models = {}

    def train(self, name: Models, directory: str, epochs: int = 25, batch: int = -1) -> ModelData:
        new_dir = "models/" + name

        if os.path.exists(new_dir):
            shutil.rmtree(new_dir)

        if os.path.exists("runs"):
            shutil.rmtree("runs")

        self.base_model.train(data=directory + "/data.yaml", epochs=epochs, imgsz=1280, batch=batch)
        prod_model_path = "runs/detect/train/weights/best.pt"
        os.makedirs(new_dir)

        shutil.move(prod_model_path, new_dir)
        os.rename(new_dir + "/best.pt", new_dir + "/" + name + ".pt")
        shutil.rmtree("runs")
        self.models[name] = ModelData(name, new_dir + "/" + name + ".pt")
        return self.models[name]

    def load(self, name: Models) -> ModelData:
        model_path = "models/" + name + "/" + name + ".pt"
        if os.path.isfile(model_path):
            self.models[name] = ModelData(name, model_path)
            return self.models[name]

    def get(self, name: Models) -> ModelData:
        return self.models[name]
