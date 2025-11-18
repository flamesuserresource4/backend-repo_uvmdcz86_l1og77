from pydantic import BaseModel, Field
from typing import List, Optional

# Solo Leveling specific schemas

class Hunter(BaseModel):
    name: str
    rank: str = Field(..., pattern="^[S|A|B|C|D|E]$")
    class_type: str  # e.g., Assassin, Mage, Tank
    level: int = Field(1, ge=1)
    skills: List[str] = []
    guild: Optional[str] = None
    power_score: int = Field(0, ge=0)
    biography: Optional[str] = None

class Guild(BaseModel):
    name: str
    leader: str
    members: List[str] = []
    region: Optional[str] = None
    reputation: int = Field(0, ge=0, le=100)

class Quest(BaseModel):
    title: str
    difficulty: str  # E, D, C, B, A, S
    reward_gold: int = Field(0, ge=0)
    time_limit_seconds: int = Field(0, ge=0)
    recommended_rank: str

class Shadow(BaseModel):
    name: str
    type: str  # Knight, Assassin, Mage, Tank
    grade: str  # Elite, General, Monarch-level
    special_ability: Optional[str] = None

class User(BaseModel):
    email: str
    password_hash: str
    display_name: str
    hunter_rank: str = "E"
    achievements: List[str] = []
