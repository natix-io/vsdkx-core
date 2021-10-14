from abc import ABC, abstractmethod

from vsdkx.core.structs import Inference, AddonObject, FrameObject


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
    def inference(self, frame: FrameObject) -> Inference:
        """
        This method will be called by EventDetector to receive inference result
        from model drivers

        Args:
            frame (FrameObject): the frame data

        Returns:
            (Inference): the result of the model driver
        """
        pass

    def draw(self, frame: FrameObject, inference: Inference):
        """
        This method will be called by EventDetector only if debug is true in
        model_settings

        Args:
            frame (FrameObject): the frame data
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

    def pre_process(self, addon_object: AddonObject) -> AddonObject:
        """
        This method would be called by EventDetector before calling the
        inference method of model driver

        Args:
            addon_object (AddonObject): the frame data

        Returns:
            (AddonObject): the numpy data of new frame
        """
        return addon_object

    @abstractmethod
    def post_process(self, addon_object: AddonObject) -> AddonObject:
        """
        This method will be called by EventDetector after calling the inference
        method of model driver

        Args:
            addon_object (AddonObject): object containing frame,
            inference result and data shared from other addons

        Returns:
            (AddonObject): addon object with added information
        """
        return addon_object
