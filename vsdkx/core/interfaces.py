from abc import ABC, abstractmethod

from numpy import ndarray

from vsdkx.core.structs import Inference


class ModelDriver(ABC):

    @abstractmethod
    def __init__(self,
                 model_config: dict,
                 profile: dict,
                 drawing_config: dict):
        pass

    @abstractmethod
    def inference(self, frame: ndarray) -> Inference:
        pass

    def draw(self, frame: ndarray, inference: Inference):
        pass


class Addon(ABC):

    @abstractmethod
    def __init__(self, addon_config: dict):
        pass

    @abstractmethod
    def pre_process(self, frame: ndarray) -> ndarray:
        pass

    @abstractmethod
    def post_process(self, inference: Inference) -> Inference:
        pass
