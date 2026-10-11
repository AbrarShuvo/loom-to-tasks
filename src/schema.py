from typing import Literal
from pydantic import BaseModel


class Task(BaseModel):
    title: str
    owner: str
    owner_confirmed: bool
    deadline: str
    priority: Literal["high", "medium", "low", "unknown"]


class Extraction(BaseModel):
    summary: str
    decisions: list[str]
    tasks: list[Task]
    blockers: list[str]