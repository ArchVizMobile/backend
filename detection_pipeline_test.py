import logging
from ml.common.ModelTrainer import ModelTrainer, Models
from ml.common.Pipeline import PipelineBuilder
from ml.stairs.StairService import StairService, StairDetectionRequest
from ml.wallfeatures.WallfeatureService import WallFeatureService, WallFeatureDetectionRequest
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
stair_model = trainer.load(Models.STAIRS)
wallfeatures_model = trainer.load(Models.WALLFEATURES)

stair_service = StairService(stair_model)
wallfeatures_service = WallFeatureService(wallfeatures_model)

detection_pipeline = PipelineBuilder().with_step(stair_service).with_step(wallfeatures_service).build()

result = detection_pipeline.execute("pdfS510-3.jpg")

logging.info(result)
