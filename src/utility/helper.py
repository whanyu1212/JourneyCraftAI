import yaml


def parse_yaml_file(file_path):
    """
    Parse a YAML file and return the data as a dictionary.

    Args:
    - file_path (str): The path to the YAML file to be parsed.

    Returns:
    - dict: The data from the YAML file as a dictionary.
    """
    with open(file_path, "r") as file:
        data = yaml.safe_load(file)
    return data


def load_agent_config(file_path):
    """
    Load agent configuration from the YAML file.

    Returns:
    - dict: A dictionary containing llm_config and code_execution_config.
    """
    cfg = parse_yaml_file(file_path)
    return {
        "llm_config": cfg["llm_config"],
        "code_execution_config": cfg["code_execution_config"],
    }
