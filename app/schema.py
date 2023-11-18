from typing import Optional
from sqlmodel import SQLModel, Field

class ScoreObject(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    score: int
    creation_date: int
    achievement_date: Optional[int]
    achieved: bool = Field(default=False)


class Prize(ScoreObject, table=True):
    pass


class Reward(ScoreObject, table=True):
    pass


class Penalty(ScoreObject, table=True):
    pass
