"""
Defines the Object class and useful methods surrounding it.
"""

from dataclasses import dataclass
from pathlib import Path
import yaml

@dataclass
class Object:
    """
    Represents a single object stimulus as part of a relation.
    Used for sentences and visual scenes alike.

    Attributes:
        name = Identfier of the object (e.g. "apple")
        cat = Category the object belongs to (e.g. "fruit")
        mesh = Optional path to the object's 3D mesh file
        role = Optional role in a trial, dependent on relation (e.g. either "higher" or "lower" in "above" relation)
    """

    name: str
    cat: str

    mesh: Path | None = None
    role: str = ""


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
        
