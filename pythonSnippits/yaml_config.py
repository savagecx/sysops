import os
import yaml


def read_yaml_config(filename: str = "config.yaml") -> yaml.YAMLObject:
    """Reads a YAML configuration file in as a YAML object

    Parameters
    ----------
    filename: str, optional
        The YAML configuration filename (default is config.yaml)

    Returns
    -------
    cfg: YAMLObject
        A YAML object listing the script configuration values

    Raises
    ------
    FileNotFoundError
        If a configuration file is not in the current script directory
    """

    # Build file locations based on current script file path
    script_dir = os.path.dirname(__file__)
    config_path = os.path.join(script_dir, filename)

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found at: {config_path}")

    # Read Config File
    with open(config_path, "r") as config_file:
        cfg = yaml.load(config_file, Loader=yaml.FullLoader)

    return cfg
