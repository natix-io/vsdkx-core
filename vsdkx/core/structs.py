from dataclasses import dataclass, field
from numpy import ndarray


@dataclass
class Inference:
    """
    This is the structure of inference result
    """
    boxes: ndarray = field(default_factory=lambda: [])
    classes: ndarray = field(default_factory=lambda: [])
    scores: ndarray = field(default_factory=lambda: [])
    extra: dict = field(default_factory=lambda: {})
