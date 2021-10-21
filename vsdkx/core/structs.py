from dataclasses import dataclass, field
from numpy import ndarray
from typing import Optional


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


@dataclass
class AddonObject:
    """
    Encapsulating data for transmission between addons

    Attributes:
        frame (ndarray): frame image
        inference (Inference): AI inference result
        shared (dict): data to be shared between addons
    """
    frame: ndarray
    inference: Optional[Inference]
    shared: dict = field(default_factory=lambda: {})


@dataclass
class FrameObject:
    """
    Encapsulating data for transmission between models

    Attributes:
        frame (ndarray): frame image
        metadata (dict): metadata dictionary

    """
    frame: ndarray
    metadata: Optional[dict]
