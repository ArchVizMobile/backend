from collections import deque


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
    def __init__(self, services):
        self.services = list(services)

    def execute(self, args):
        for service in self.services:
            service(args)


class Pipeline:
    def __init(self):
        self.steps = list()

    def add(self, service):
        self.steps.append(PipelineStep(service))

    def execute(self, image):
        for service in self.steps:
            service.execute(image)
