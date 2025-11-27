from pydantic import BaseModel, field_serializer
from typing import List
from networkx import Graph
from enum import Flag


class ModelStatus(Flag):
    """
    Status of a model.
    """
    
    OPTIMAL = 1
    FEASIBLE = 2
    OTHER = 4
    UNKWOWN = 8
    

class Solution(BaseModel):
    """
    A class representing a solution to the graph coloring problem

    Attributes:
        graph: a copy of the graph, where each node has the attribute color
        colors: number of colors used in the coloring of the `graph`
        status: status of the model (see `ModelStatus`)
    """
    
    graph: Graph
    colors: int | float
    status: ModelStatus
    
    class Config:
        arbitrary_types_allowed = True