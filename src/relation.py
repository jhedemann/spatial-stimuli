"""
Defines the Relation class and useful methods surrounding it.
"""

from pathlib import Path
from entity import Object
from typing import Literal, get_args

spatial_rels = Literal[
    "above",
    "below",
    "to the left of",
    "to the right of",
    "in front of",
    "behind",
]

allowed_rels = set(get_args(spatial_rels))

class Relation:
    """
    Represents a spatial relation between two objects.
    Used for sentences and visual scenes alike.

    Attributes:
        first_obj = First object (e.g. "apple" Object)
        second_obj = Second object (e.g. "hat" Object)
        rel = Relational word determining the relation (e.g. "above")
    """

    def __init__(
            self,
            first_obj: Object,
            second_obj: Object,
            rel: allowed_rels):

        if rel not in allowed_rels:
            raise ValueError(
                f"Relation '{rel}' is invalid. Expected one of: {sorted(ALLOWED_RELS)}"
                )
        else:
            self.rel = rel

        self.first_obj = first_obj
        self.second_obj = second_obj

        match rel:
            case "above":
                self.first_obj.role = "higher"
                self.second_obj.role = "lower"
            case "below":
                self.first_obj.role = "lower"
                self.second_obj.role = "higher"
            case "to the left of":
                self.first_obj.role = "left"
                self.second_obj.role = "right"
            case "to the right of":
                self.first_obj.role = "right"
                self.second_obj.role = "left"
            case "in front of":
                self.first_obj.role = "front"
                self.second_obj.role = "hind"
            case "behind":
                self.first_obj.role = "hind"
                self.second_obj.role = "front"

    def to_sentence(self) -> str:
        return f"The {self.first_obj.name} is {self.rel} the {self.second_obj.name}."

