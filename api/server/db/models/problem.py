
from fastapi import Body
from pydantic import BaseModel


class ProblemSchema(BaseModel):
    authorId: str
    title: str 
    description: str
    example_input: str
    example_output: str
    tags: list[str] | None

    class Config:
        schema_extra = {
            "example": {
                "authorId": "",
                "title": "Rudolph and Cut the Rope",
                "description":
                    "There are nnails driven into the wall, the ith nail is drive...",
                "example_input": "4 3 4 3 3 1 1 2",
                "example_output": "2 2 3 0",
                "tags": ["implementation", "math"]
            }
        }


class UpdateUserSchema(BaseModel):
    authorId: str | None
    title: str | None
    description: str | None
    example_input: str | None
    example_output: str | None
    tags: list[str] | None

    class Config:
        schema_extra = {
            "example": {
                "title": "Rudolph and Cut the Rope 4",
            }
        }
