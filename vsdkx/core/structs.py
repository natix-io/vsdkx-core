from dataclasses import dataclass, field
from numpy import ndarray


@dataclass
class Inference:
    """
    This is the structure of inference result

    Attributes:
        boxes (ndarray): numpy array of box coordinates
        classes (ndarray): class ids for each bounding box
        scores (ndarray): confidence scores for each bounding box
        extra (dict): a dictionary to pass data between model driver and addonsxxxx
    """
    boxes: ndarray = field(default_factory=lambda: [])
    classes: ndarray = field(default_factory=lambda: [])
    scores: ndarray = field(default_factory=lambda: [])
    extra: dict = field(default_factory=lambda: {})
