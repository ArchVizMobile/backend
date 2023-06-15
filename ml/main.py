import logging

from common.ModelTrainer import ModelTrainer, Models
from common.Pipeline import PipelineBuilder
from stairs.StairService import StairService, StairDetectionRequest

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
# stair_model = trainer.train(Models.STAIRS, "stairs/di.v2i.yolov8", 100)
stair_model = trainer.load(Models.STAIRS)

stair_service = StairService(stair_model)
result = stair_service.detect(StairDetectionRequest("stairs/data"))

logging.info(result)

# pipeline = PipelineBuilder().with_step(stair_service).with_step(stair_service).build()
# pipeline.execute("image.png")