from pydantic import BaseModel, Field
from typing import List


class StarNode(BaseModel):
    id: str
    title: str
    category: str
    probability: float
    x: float
    y: float
    size: float = 10
    color: str = "#ffffff"


class StarEdge(BaseModel):
    source: str
    target: str
    path_type: str = "main"


class StarMapResponse(BaseModel):
    nodes: List[StarNode] = Field(default_factory=list)
    edges: List[StarEdge] = Field(default_factory=list)
    current_position: dict = Field(default_factory=dict)
