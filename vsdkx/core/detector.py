import importlib
import logging
import os
import time
from dataclasses import asdict

import cv2
from numpy import ndarray

from vsdkx.core.interfaces import ModelDriver, Addon
from vsdkx.core.structs import AddonObject, FrameObject
from vsdkx.core.util import io
from vsdkx.core.util.drawing import draw_zones, draw_boxes, show_window
from vsdkx.core.util.io import get_env_dict
from vsdkx.core.util.model import box_sanity_check

LOG_TAG = "EventDetector"


class EventDetector:
    """
    This class connects to the model driver and addons based on the config
    dictionary that it is initialized with and with detect method it returns
    the inference result
    """

    def __init__(self,
                 system_config: dict):
        """
        Initialize with the config dictionary

        Args:
            system_config: you can see the structure of this dictionary
            in README.md file
        """
        self._logger = logging.getLogger(LOG_TAG)
        model_class = get_env_dict(system_config,
                                   "model.class")
        model_settings = get_env_dict(system_config,
                                      "model.settings")
        model_profile = get_env_dict(system_config,
                                     "model.profile")
        self.image_type = get_env_dict(system_config,
                                       "image_type",
                                       default='BGR')
        self._debug = get_env_dict(system_config,
                                   "model.debug",
                                   False)
        self._drawing_config = get_env_dict(system_config, "drawing", {})
        profile_path = os.path.join("vsdkx", "model", "profile.yaml")
        profile = io.import_yaml(profile_path)
        model_config = get_env_dict(profile, model_profile)
        module_name, class_name = model_class.rsplit(".", 1)
        module = importlib.import_module(module_name)
        class_ = getattr(module, class_name)
        self.model_driver: ModelDriver = class_(model_settings,
                                                model_config,
                                                self._drawing_config)
        self._logger.info(f"Loaded driver {self.model_driver}, "
                          f"with settings {model_settings}, "
                          f"with config {model_config}, "
                          f"with drawing {self._drawing_config}")
        addons_config = get_env_dict(system_config,
                                     "addons",
                                     {})
        self.addons: [Addon] = []
        for _, config in addons_config.items():
            class_loader = get_env_dict(config, "class")
            module_name, class_name = class_loader.rsplit(".", 1)
            module = importlib.import_module(module_name)
            class_ = getattr(module, class_name)
            self.addons.append(class_(config, model_settings, model_config,
                                      self._drawing_config))
        self._logger.info(f"Loaded addons {self.addons}")

    def detect(self, frame: ndarray, metadata: dict = {}) -> dict:
        """
        method to use model driver to get the inference result and apply all
        the addons to the frame and inference.

        Args:
            frame: the frame data

        Returns:
            (dict): the dictionary which hase inference result in
        """
        if self.image_type == 'BGR':
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        addon_stamp = time.time()
        addon_object = AddonObject(frame=frame, inference=None,
                                   shared=metadata)
        for addon in self.addons:
            stamp = time.time()
            addon_object = addon.pre_process(addon_object)
            self._logger.debug(f"{addon} preprocessed in "
                               f"{time.time() - stamp}")
        self._logger.debug(f"All addons preprocessed in "
                           f"{time.time() - addon_stamp}")
        frame = addon_object.frame
        stamp = time.time()
        frame_object = FrameObject(frame, metadata)
        inference = self.model_driver.inference(frame_object)
        inference.boxes = box_sanity_check(inference.boxes,
                                           frame.shape[1],
                                           frame.shape[0])
        self._logger.debug(f"Inference result in "
                           f"{time.time() - stamp}")
        addon_stamp = time.time()
        addon_object.inference = inference
        for addon in self.addons:
            stamp = time.time()
            addon_object = addon.post_process(addon_object)
            self._logger.debug(f"{addon} post processed in "
                               f"{time.time() - stamp}")

        self._logger.debug(f"All addons post processed in "
                           f"{time.time() - addon_stamp} {inference}")
        inference = addon_object.inference
        frame_object.frame = addon_object.frame
        if self._debug:
            draw_zones(self._drawing_config, addon_object.frame)
            draw_boxes(self._drawing_config,
                       addon_object.frame,
                       inference.boxes,
                       inference.scores,
                       inference.classes)
            self.model_driver.draw(frame_object, inference)
            show_window(frame)
        return asdict(inference)
