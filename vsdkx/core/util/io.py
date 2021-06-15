import yaml
import os


def import_yaml(path):
    """
    Imports the contents of an entire yaml file into a dictionary
    for future use

    Args:
        path (string): path to a yaml file

    Returns:
        (dict): dictionary of yaml key-value pairs
    """
    with open(path) as config_file:
        config_data = yaml.load(config_file, Loader=yaml.FullLoader)
    return config_data


def get_env(file: str, key: str, default=None):
    """
    This function would just ease the process to get config parameters.

    Args:
        file (str): file path of yaml file
        key (str): key of config in yaml file with dot as delimiter.
        for example
            key can be processors.ai_processors.processor.uri to get the uri
             parameter of that processor
        default (Any|None):
            if there is no key in yaml file then this will be returned else
            None

    Returns
        (Any): the value of the key in yaml file if present else
        default value
    """
    if file is None:
        return default
    try:
        node = import_yaml(file)
    except FileNotFoundError:
        return default
    return get_env_dict(node, key, default)


def get_env_dict(node: dict, key: str, default=None):
    """
    This function would just ease the process to get config parameters
    from dict

    Args:
        node: the dictionary that we want to extract the key from
        key (str): key of config in yaml file with dot as delimiter.
        for example
            key can be processors.ai_processors.processor.uri to get the uri
             parameter of that processor
        default (Any|None):
            if there is no key in yaml file then this will be returned else
            None

    Returns
        (Any): the value of the key in yaml file if present else
        default value

    """
    if node is None:
        return default
    path = key.split(".")
    for p in path:
        if p in node:
            node = node[p]
        else:
            return default
    if isinstance(node, str):
        if node.startswith("${") and node.endswith("}"):
            return os.getenv(node[2:-1], default)
    return node
