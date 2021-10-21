import importlib


def import_default_settings(path):
    settings_file, settings_var = path.rsplit(".", 1)
    module = importlib.import_module(settings_file)
    default_settings = getattr(module, settings_var)
    return default_settings
