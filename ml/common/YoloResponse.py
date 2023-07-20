from dataclasses import dataclass


@dataclass
class YoloResponse:
    xmin: float
    xmax: float
    ymin: float
    ymax: float
    object: str