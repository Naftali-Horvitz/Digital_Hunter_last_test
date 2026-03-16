from pydantic import BaseModel, Field
from typing import Optional, Literal


class Intelligence(BaseModel):
    timestamp: str
    attack_id: str
    entity_id: str
    result: bool