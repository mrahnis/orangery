def load_config(json_f: str) -> dict:
    """Load a json file containing configuration data

    Parameters:
        json_f: path to json file

    Returns:
        config (dict): dictionary of configuration data

    """
    import json

    with open(json_f, 'r') as json_src:
        config = json.load(json_src)
    return config
