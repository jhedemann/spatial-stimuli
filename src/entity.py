"""
Defines the Object class and useful methods surrounding it.
"""

from dataclasses import dataclass
from pathlib import Path
import yaml

@dataclass
class Object:
    name: str  # "apple" for an apple
    cat: str  # "fruit" for an apple

    mesh: Path | None = None # path to mesh file of the object
    role: str = "" # depending on relation (either "higher" or "lower" in "above" relation)


def load_all_objs(path = Path | str):
    """Load all objets from YAML file into dictionary with their names as keys."""
    
    with open(path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    return {item["name"]:Object(**item) for item in config["objects"]}

def load_obj_by_name(path = Path | str, target_name = str):
    """Load the single object that matches target_name from YAML file."""

    with open(path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    for item in config["objects"]:
        if item["name"]==target_name:
            return Object(**item)
        
