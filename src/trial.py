"""
Defines the Trial class and useful methods surrounding it.
"""

from pathlib import Path
from relation import Relation
from typing import Literal, get_args

types = Literal[
    "sentence",
    "scene"
]

allowed_types = set(get_args(types))

class Trial:
    """
    Specifies a single trial.

    Attributes:
        id = Index of trial embedded in an experiment
        type = Presentation type (either "sentence" or "scene")
        relation = Relation to be presented
    """

    def __init__(
            self,
            id: int,
            type: allowed_types,
            relation: Relation):

        if type not in allowed_types:
            raise ValueError(
                f"Type '{type}' is invalid. Expected one of: {sorted(allowed_types)}"
                )
        else:
            self.type = type

        self.id = id
        self.relation = relation

    def __repr__(self) -> str:
        return f"Trial object number {self.id} of type {self.type} with relation '{self.relation.to_sentence()}'."