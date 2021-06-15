import tensorflow as tf


def load_tflite(tf_model_path):
    """
    Loads tflite model from a given path

    Args:
        tf_model_path (str): Path to the model

    Returns:
        (interpreter, input_details, output_details):
        tf.lite.Interpreter, interpreter's input and output details
    """
    # Load the tflite model and allocate tensors
    interpreter = tf.lite.Interpreter(model_path=tf_model_path)
    interpreter.allocate_tensors()
    # Get input and output tensors.
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    return interpreter, input_details, output_details


def box_sanity_check(box, width, height):
    """
    Performing a sanity check on the detected bounding
    boxes, to prevent negative coordinates from being drawn
    Args:
        box (np.array): 1D array with the box x1y1x2y2 coordinates
        width (float): The width of the box
        height (float): The height of the box

    Returns:
        (np.array): np.array with positive box coordinates
    """
    xmin = max(0, int(box[0]))
    ymin = max(0, int(box[1]))
    xmax = min(width, int(box[2]))
    ymax = min(height, int(box[3]))

    # Checking if ymin and xmin are equal or bigger than ymax and xmax
    # If true, we set them to 10, a higher number than the minimum of
    # xmin and ymin which are set to 0.

    if xmin >= xmax:
        xmax = min(xmin + 10, width)
    if ymin >= ymax:
        ymax = min(ymin + 10, height)
    return [xmin, ymin, xmax, ymax]
