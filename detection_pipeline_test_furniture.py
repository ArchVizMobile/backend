import logging
from ml.common.ModelTrainer import ModelTrainer, Models
from ml.common.Pipeline import PipelineBuilder
from ml.stairs.StairService import StairService, StairDetectionRequest
from ml.furniture.FurnitureService import FurnitureService, FurnitureDetectionRequest

logging.basicConfig(
    encoding='utf-8',
    level=logging.INFO,
    format='[%(asctime)s][%(levelname)s]: %(message)s',
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)

trainer = ModelTrainer()
# stair_model = trainer.train(Models.STAIRS, "ml/stairs/di.v2i.yolov8", 100)
furniture_model = trainer.load(Models.FURNITURE)

furniture_service = FurnitureService(furniture_model)

detection_pipeline = PipelineBuilder().with_step(furniture_service).build()

result = detection_pipeline.execute("ml/furniture/data/furniture_test.png")

logging.info(result)
