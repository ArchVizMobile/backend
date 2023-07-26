import logging
from typing import List
from ml.common.ModelTrainer import ModelTrainer, Models
from ml.common.Pipeline import PipelineBuilder
from ml.stairs.StairService import StairService, StairDetectionRequest
from ml.wallfeatures.WallfeatureService import WallFeatureService, WallFeatureDetectionRequest
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

# takes an array of paths to images
def runPipeline( paths: List[str]):
    trainer = ModelTrainer()
    stair_model = trainer.load(Models.STAIRS)
    wallfeatures_model = trainer.load(Models.WALLFEATURES)
    furniture_model = trainer.load(Models.FURNITURE)

    furniture_service = FurnitureService(furniture_model)
    stair_service = StairService(stair_model)
    wallfeatures_service = WallFeatureService(wallfeatures_model)

    detection_pipeline = PipelineBuilder().with_step(stair_service).with_step(wallfeatures_service).with_step(furniture_service).build()

    #result = detection_pipeline.execute("ml/stairs/data/csm_grundriss-kern-haus-aura-einliegerwohnung-dachgeschoss_9b507b4138_jpg.rf.5a6c9493bcf127b5d900e303db9c2347.jpg")
    result = detection_pipeline.execute(*paths)

    logging.info(result)
    return result
