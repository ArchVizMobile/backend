import json
import logging
from collections import deque

import jsonpickle


class PipelineBuilder:
    def __init__(self):
        self.steps = deque()

    def with_step(self, services):
        self.steps.append(PipelineStep(services))
        return self

    def build(self):
        pipeline = Pipeline()
        for step in self.steps:
            pipeline.add(step)
        return pipeline


class PipelineStep:
    def __init__(self, service):
        self.model = service.model_data.model
        self.service = service

    def execute(self, args):
        return self.service.detect(args)


class Pipeline:
    def __init__(self):
        self.steps = list()

    def add(self, service):
        self.steps.append(service)

    def execute(self, *images):
        floors = []
        for image in images:
            floor = {}
            for service in self.steps:
                logging.info("test")
                floor[service.model] = service.execute(image)
        floors.append(floor)
        return jsonpickle.encode(floors, unpicklable=False)
