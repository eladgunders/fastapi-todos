from pydantic import BaseModel


class PriorityOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
