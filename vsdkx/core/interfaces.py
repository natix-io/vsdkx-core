from abc import ABC, abstractmethod

from numpy import ndarray

from vsdkx.core.structs import Inference


class ModelDriver(ABC):
    """
    Interface for all model drivers
    """

    @abstractmethod
    def __init__(self,
                 model_settings: dict,
                 model_config: dict,
                 drawing_config: dict):
        """
        Initialize model driver with model_settings, model_config and
        drawing_config

        Args:
            model_settings: settings to pass to the driver
            model_config: configuration of the model that we want to use
            drawing_config: the configuration of the drawing section
        """
        pass

    @abstractmethod
    def inference(self, frame: ndarray) -> Inference:
        """
        This method will be called by EventDetector to receive inference result
        from model drivers

        Args:
            frame (ndarray): the frame data

        Returns:
            (Inference): the result of the model driver
        """
        pass

    def draw(self, frame: ndarray, inference: Inference):
        """
        This method will be called by EventDetector only if debug is true in
        model_settings

        Args:
            frame (ndarray): the frame data
            inference (Inference): the result if the model driver
        """
        pass


class Addon(ABC):
    """
    Interface for all addons
    """

    @abstractmethod
    def __init__(self, addon_config: dict, model_settings: dict,
                 model_config: dict,
                 drawing_config: dict):
        """
        Initialize with addon_config, model_settings, model_config,
        drawing_config

        Args:
            addon_config (dict): configuration data related to this addon
            model_settings (dict): settings that has passed to model driver
            model_config (dict): configuration of the model that used
            for inference
            drawing_config (dict): configuration for drawing section
        """
        pass

    def pre_process(self, frame: ndarray) -> ndarray:
        """
        This method would be called by EventDetector before calling the
        inference method of model driver

        Args:
            frame (ndarray): the frame data

        Returns:
            (ndarray): the numpy data of new frame
        """
        return frame

    @abstractmethod
    def post_process(self, frame: ndarray, inference: Inference) -> Inference:
        """
        This method will be called by EventDetector after calling the inference
        method of model driver

        Args:
            frame (ndarray): the frame data
            inference (Inference): the result of the inference from
            model driver

        Returns:
            (Inference): new inference result. addons can put information in
            extra section of inference structure
        """
        pass
