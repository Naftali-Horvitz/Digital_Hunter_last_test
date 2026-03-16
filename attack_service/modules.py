from pydantic import BaseModel, Field
from typing import Optional, Literal


class Intelligence(BaseModel):
    timestamp: str
    attack_id: str
    entity_id: str
    weapon_type: Literal[
        "AGM-114 Hellfire",
        "GBU-39 SDB",
        "Delilah Missile",
        "SPICE-250",
        "Popeye AGM",
        "Griffin LGM",
    ]
