from abc import ABC, abstractmethod
from networkx import Graph
import math

from utils.data_schema import Solution
class GCSolver(ABC):
    
    def __init__(self, instance: Graph,  number_of_colors: int = -1):
        pass
    
    @abstractmethod
    def generate_graph(self):
        pass
    
    @abstractmethod
    def get_graph(self):
        pass
    
    @abstractmethod
    def solve(self, timelimit: float = math.inf) -> Solution:
        pass