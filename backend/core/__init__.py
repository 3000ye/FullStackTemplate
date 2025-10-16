import os
import toml


base_config_path = os.path.join(os.path.dirname(__file__), "../config/base.toml")
with open(base_config_path, "r", encoding="utf-8") as file:
    base_config = toml.load(file)
