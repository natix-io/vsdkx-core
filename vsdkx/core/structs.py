from dataclasses import dataclass, field
from numpy import ndarray


@dataclass
class Inference:
    """
    This is the structure of inference result
    """
    boxes: ndarray = None
    classes: ndarray = None
    scores: ndarray = None
    extra: dict = field(default={})