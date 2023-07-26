import enum
from pydantic import BaseModel, Field

# schemas


class SolutionSchema(BaseModel):
    language: str = Field(..., min_length=3, max_length=50)
    language_version: str = Field(..., min_length=3, max_length=50)
    code: str = Field(..., min_length=3, max_length=10000)

    class Config:
        schema_extra = {
            "example": {
                "language": "python",
                "language_version": "3.9.1",
                "code": "print('Hello World')",
            }
        }


class SolutionDBSchema(SolutionSchema):
    id: str
    authorId: str

    class Config:
        schema_extra = {
            "example": {
                "id": "60b6d1a7e6b6f9f9f9f9f9f9",
                "authorId": "60b6d1a7e6b6f9f9f9f9f9f9",
                "language": "python",
                "language_version": "3.9.1",
                "code": "print('Hello World')",
            }
        }


class status_code(str, enum.Enum):
    AC = "AC"
    WA = "WA"
    TLE = "TLE"
    MLE = "MLE"
    RE = "RE"


class SolutionResultSchema(BaseModel):
    status: str = Field(..., min_length=2, max_length=3)
    run_time: float = Field(..., gt=0)
    memory: int = Field(..., gt=0)

    class Config:
        schema_extra = {
            "example": {
                "status": "AC",
                "run_time": 0.001,
                "memory": 100,
            }
        }


# helpers

def dict_to_solution_db_schema(solution: dict) -> SolutionDBSchema:
    return SolutionDBSchema(
        id=str(solution["_id"]),
        authorId=str(solution["authorId"]),
        language=solution["language"],
        language_version=solution["language_version"],
        code=solution["code"],
    )
