from pydantic import BaseModel


class PriorityRead(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
