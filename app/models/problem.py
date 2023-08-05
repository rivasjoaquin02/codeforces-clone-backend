from pydantic import BaseModel, Field

# schemas


class ProblemSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=1000)
    inputExample: str
    outputExample: str
    tags: list[str] | None
    difficulty: str

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Rudolph and Cut the Rope",
                "description": "There are nnails driven into the wall, the ith nail is drive...",
                "inputExample": "4 3 4 3 3 1 1 2",
                "outputExample": "2 2 3 0",
                "tags": ["implementation", "math"],
                "difficulty": "easy",
            }
        }


class ProblemDBSchema(ProblemSchema):
    id: str
    authorId: str


class UpdateProblemSchema(BaseModel):
    title: str | None
    description: str | None
    inputExample: str | None
    outputExample: str | None
    tags: list[str] | None
    difficulty: str | None

    class Config:
        json_schema_extra = {
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
        inputExample=problem["inputExample"],
        outputExample=problem["outputExample"],
        tags=problem["tags"],
        difficulty=problem["difficulty"],
    )
