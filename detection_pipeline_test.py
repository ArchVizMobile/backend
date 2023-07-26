import logging
from ml.common.ModelTrainer import ModelTrainer, Models
from ml.common.Pipeline import PipelineBuilder
from ml.stairs.StairService import StairService, StairDetectionRequest

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

stair_service = StairService(stair_model)

detection_pipeline = PipelineBuilder().with_step(stair_service).with_step(stair_service).build()

result = detection_pipeline.execute("ml/stairs/data/csm_grundriss-kern-haus-aura-einliegerwohnung-dachgeschoss_9b507b4138_jpg.rf.5a6c9493bcf127b5d900e303db9c2347.jpg")

logging.info(result)
