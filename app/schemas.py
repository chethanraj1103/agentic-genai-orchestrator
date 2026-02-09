from pydantic import BaseModel
from typing import List, Any

class TaskRequest(BaseModel):
    task: str

class Step(BaseModel):
    thought: str
    action: str
    observation: str

class TaskResponse(BaseModel):
    result: Any
    steps: List[Step]
