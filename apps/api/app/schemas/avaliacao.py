from pydantic import BaseModel


class ResponderAvaliacaoIn(BaseModel):
    texto: str
