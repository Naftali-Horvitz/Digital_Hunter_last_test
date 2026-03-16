from pydantic import BaseModel, Field
from typing import Optional, Literal

class Intelligence(BaseModel):
    timestamp : str
    signal_id: str
    entity_id: str
    reported_lat: float
    reported_lon: float
    signal_type: Literal["SIGINT", "VISINT", "HUMINT"]
    priority_level: Optional[int] = Field(gt=0, lt=6, default=99)
    