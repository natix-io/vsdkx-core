import cv2
import numpy as np

from vsdkx.core.structs import Inference


def visualize(frame: np.array, inference_obj: Inference):
    """
    Function for visualizing input
    Args:
        frame: input frame
        inference_obj: inference object

    Returns:
        None
    """
    boxes = inference_obj.boxes
    for box in boxes:
        frame = cv2.rectangle(frame, tuple(box[:2]), tuple(box[2:]),
                              (0, 255, 0))
    cv2.imshow('Input Frame', frame)
    cv2.waitKey(1)
