import argparse
import logging
import time
from typing import Callable
import cv2
from ai_connector.server import Server
from numpy import ndarray
from vsdkx.core.util import io
from vsdkx.core.detector import EventDetector
from vsdkx.core.structs import Inference

LOG_TAG = "SimpleRunner"


class SimpleRunner:

    def __init__(self,
                 draw_method: Callable[[ndarray, Inference], None] = None):
        self._draw_method = draw_method
        self._logger = logging.getLogger(LOG_TAG)

    def _run_inference(self, detector: EventDetector, image: ndarray):
        result = detector.detect(image)
        if self._draw_method is not None:
            self._draw_method(image, result)

    def run(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--no-server', default=False, action='store_true',
                            help='set True to run without gRPC')
        parser.add_argument('--image-path', type=str,
                            help='path to your image.')
        parser.add_argument('--video-path', type=str, default='0',
                            help='path to your video, `0` means to use camera')
        parser.add_argument('--config-path', type=str, default='0',
                            help='path to system config')

        args = parser.parse_args()

        # Run people detection as a gRPC server
        if not args.no_server:
            Server.run(EventDetector)
        else:
            if args.config_path is not None:
                detector = EventDetector(
                    io.import_yaml(args.config_path))
                # Run inference on a single image
                if args.image_path is not None:

                    # Time stamp for performance reporting
                    start_stamp = time.time()

                    # Read the image
                    image = cv2.imread(args.image_path)
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                    # Time stamp for performance reporting
                    read_stamp = time.time()

                    # Run the inference
                    self._run_inference(detector, image)

                    # Time stamp for performance reporting
                    end_stamp = time.time()

                    self._logger.debug(f'Read time {read_stamp - start_stamp}')
                    self._logger.debug(f'Done {end_stamp - start_stamp}')

                elif args.video_path is not None:
                    # Check if video_path is valid
                    try:
                        video_path = int(args.video_path)
                    except ValueError:
                        video_path = args.video_path

                    cap = cv2.VideoCapture(video_path)
                    assert cap.isOpened(), "Video open failed."
                    status = True
                    start_stamp = time.time()
                    while status:
                        # Time stamp for performance reporting
                        read_start_stamp = time.time()
                        status, frame = cap.read()
                        # Frame to RGB
                        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        read_end_stamp = time.time()
                        self._run_inference(detector, image)
                        self._logger.debug(
                            f'Read time {read_end_stamp - read_start_stamp}')
                        status, frame = cap.read()
                    end_stamp = time.time()
                    self._logger.debug(f'Done {end_stamp - start_stamp}')

                    cap.release()
