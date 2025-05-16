import os


def abs_path(path: str):
    current_file_path = os.path.dirname(__file__)
    return os.path.join(current_file_path, path)


def get_model_and_config(path: str, model_type, config_type):
    lang_files = os.listdir(path)
    model_file = next((file for file in lang_files if file.endswith(model_type)), None)
    config_file = next((file for file in lang_files if file.endswith(config_type)), None)
    model_path = os.path.join(path, model_file)
    config_path = os.path.join(path, config_file)

    return model_path, config_path
