from numpy import ndarray
import numpy
import cv2


def draw_zones(draw_config: dict, image: ndarray):
    """
    draws zones as configured in draw_config

    Args:
        draw_config (dict): configuration for the drawing like font and colors
        image (ndarray): raw frame of a video
    """
    for zone in draw_config.get("zones", []):
        zone = numpy.array(zone)

        cv2.polylines(image,
                      [zone],
                      True,
                      color=draw_config.get("zones_color", (0, 0, 0)),
                      thickness=draw_config.get("zone_thickness", 3))


def draw_boxes(
        draw_config: dict,
        image,
        boxes,
        scores=None,
        classes=None,
):
    """
    Private drawing method for boxes and labels

    Args:
        draw_config (dict): configuration for the drawing like font and colors
        image (ndarray): raw frame of a video
        boxes (ndarray): one dimensional numpy array of box coordinates
        scores (ndarray):
        classes:
    """
    if image is None or boxes is None:
        return

    height, width, _ = image.shape
    bboxes = []

    # for each list of bbox indices needed for NMS,
    # we compute a confidence interval,
    # and draw object bboxes
    for idx, box in enumerate(boxes):
        conf = ""
        if scores is not None:
            conf = float(scores[idx])
        if classes is not None:
            class_id = int(classes[idx][0])
        else:
            class_id = 0

        xmin, ymin, xmax, ymax = box[0], box[1], box[2], box[3]
        bbox = (
            [xmin, ymin, xmax, ymax], class_id)
        bboxes.append(bbox)

        label = ""

        # TODO: discuss what to do with different size bbox color change
        #  feature. This feature was used for face mask detection only
        #  and now it has to be commented out here (didn't delete before
        #  consulting) for the sake of generalisation
        box_width = xmax - xmin
        box_height = ymax - ymin
        # if bbox size is < certain threshold, make color white
        # or transparent
        # if (box_width * box_height) < (blur_threshold * width * height):
        #     color = (255, 255, 255)
        #     label = ''
        # when wearing mask
        # if classes is not None and id2class is not None:
        #     if class_id in id2class:
        #         option = id2class[class_id]
        #         color = option["color"]
        #         label = option["text"]

        rectangle_color = draw_config.get(
            "rectangle_color") or (60, 179, 113)
        box_thickness = draw_config.get(
            "box_thickness") or 3

        cv2.rectangle(image,
                      (xmin + 2, ymin - 2),
                      (xmax + 2, ymax - 2),
                      rectangle_color,
                      box_thickness)
        if label or conf:
            cv2.putText(image,
                        "%s: %.2f" % (label, conf),
                        (xmin + 2, ymin - 2),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        draw_config.get("box_font_scale", 0.8),
                        draw_config.get("text_color", (0, 0, 0)),
                        draw_config.get("box_thickness", 3))


def show_window(frame: ndarray):
    """
    Show frame in a debug window

    Args:
        frame (ndarray): the frame data
    """
    window_name = "Result"
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(window_name,
                          cv2.WND_PROP_AUTOSIZE,
                          cv2.WINDOW_AUTOSIZE)
    cv2.imshow(window_name, frame[:, :, :])
    cv2.waitKey(1)
