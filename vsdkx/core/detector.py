import importlib
import logging

from numpy import ndarray

from vsdkx.core.interfaces import ModelDriver, Addon
from vsdkx.core.util.drawing import draw_zones, draw_boxes, show_window
from vsdkx.core.util.io import get_env_dict
import os
from vsdkx.core.util import io
import time

LOG_TAG = "EventDetector"


class EventDetector:

    def __init__(self,
                 system_config: dict):
        self._logger = logging.getLogger(LOG_TAG)
        model_class = get_env_dict(system_config,
                                   "model.class")
        model_settings = get_env_dict(system_config,
                                    "model.settings")
        model_profile = get_env_dict(system_config,
                                     "model.profile")
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
            self.addons.append(class_(config))
        self._logger.info(f"Loaded addons {self.addons}")

    def detect(self, frame: ndarray):
        addon_stamp = time.time()
        for addon in self.addons:
            stamp = time.time()
            frame = addon.pre_process(frame)
            self._logger.debug(f"{addon} preprocessed in "
                               f"{time.time() - stamp}")
        self._logger.debug(f"All addons preprocessed in "
                           f"{time.time() - addon_stamp}")
        stamp = time.time()
        inference = self.model_driver.inference(frame)
        self._logger.debug(f"Inference result in "
                           f"{time.time() - stamp}")
        if self._debug:
            draw_zones(self._drawing_config, frame)
            draw_boxes(self._drawing_config,
                       frame,
                       inference.boxes,
                       inference.scores,
                       inference.classes)
            self.model_driver.draw(frame, inference)
            show_window(frame)
        addon_stamp = time.time()
        for addon in self.addons:
            stamp = time.time()
            inference = addon.post_process(inference)
            self._logger.debug(f"{addon} post processed in "
                               f"{time.time() - stamp}")
        self._logger.debug(f"All addons post processed in "
                           f"{time.time() - addon_stamp}")
