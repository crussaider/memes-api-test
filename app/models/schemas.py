from pydantic import BaseModel
from typing import List


class Meme(BaseModel):
    id: int
    title: str
    image_url: str

    class Config:
        from_attributes = True


class MemeList(BaseModel):
    memes: List[Meme]
    total: int
