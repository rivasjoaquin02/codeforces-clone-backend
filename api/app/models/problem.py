from pydantic import BaseModel, Field

# schemas


class ProblemSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=1000)
    example_input: str
    example_output: str
    tags: list[str] | None

    class Config:
        schema_extra = {
            "example": {
                "title": "Rudolph and Cut the Rope",
                "description": "There are nnails driven into the wall, the ith nail is drive...",
                "example_input": "4 3 4 3 3 1 1 2",
                "example_output": "2 2 3 0",
                "tags": ["implementation", "math"],
            }
        }


class ProblemDBSchema(ProblemSchema):
    id: str
    authorId: str


class UpdateProblemSchema(BaseModel):
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


# helpers


def dict_to_problem_db_schema(problem: dict) -> ProblemDBSchema:
    return ProblemDBSchema(
        id=str(problem["_id"]),
        authorId=str(problem["authorId"]),
        title=problem["title"],
        description=problem["description"],
        example_input=problem["example_input"],
        example_output=problem["example_output"],
        tags=problem["tags"],
    )
