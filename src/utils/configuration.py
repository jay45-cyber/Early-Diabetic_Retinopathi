"""Configuration management and YAML parser."""
from pathlib import Path
from typing import Any, Dict
import yaml


def load_yaml_config(config_path: str | Path) -> Dict[str, Any]:
    """Load and parse a YAML configuration file safely."""
    path = Path(config_path)
    if not path.is_file():
        raise FileNotFoundError(f"Configuration file not found: {path.resolve()}")

    with open(path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    if not isinstance(config, dict):
        raise ValueError(f"Invalid YAML configuration format in {path}")

    return config

