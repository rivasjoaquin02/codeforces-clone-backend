

from bson import ObjectId
from fastapi import APIRouter, Body, Depends, status

from server.db.models.problem import ProblemSchema
from server.db.models.problem_crud import add_problem, retrieve_problem, retrieve_problems
from server.db.models.user import ErrorResponseModel, ResponseModel, UserSchema
from server.routes.auth import get_current_active_user


router = APIRouter()


@router.post("/problems/create",
             status_code=status.HTTP_201_CREATED,
             response_description="Create a problem")
async def create_problem(
        problem_data=Body(),
        current_user: UserSchema = Depends(get_current_active_user)):

    problem_data = ProblemSchema(
        authorId=current_user.id,
        title=problem_data["title"],
        description=problem_data["description"],
        tags=problem_data["tags"],
        example_input=problem_data["example_input"],
        example_output=problem_data["example_output"]
    )

    problem = await add_problem(problem_data)

    if not problem:
        raise ErrorResponseModel(
            code=status.HTTP_400_BAD_REQUEST,
            message="Title already exist"
        )
    return ResponseModel(
        data=problem,
        message="Problem correctly added..."
    )


@router.get("/problems/",
            status_code=status.HTTP_200_OK,
            response_description="Gets all the problems")
async def get_problems_data():
    problems = await retrieve_problems()

    if len(problems) == 0:
        return ResponseModel(
            data=problems,
            message="Theres is no problems yet"
        )
    return ResponseModel(
        data=problems,
        message="Here you got the problems 😎"
    )


@router.get("/problems/{id}",
            status_code=status.HTTP_200_OK,
            response_description="Gets a problem")
async def get_problem_data(id: str):

    problem = await retrieve_problem("_id", ObjectId(id))
    if not problem:
        raise ErrorResponseModel(
            code=status.HTTP_400_BAD_REQUEST,
            message="The problem you're asking for does not exist..."
        )

    return ResponseModel(
        data={**problem, "_id": str(problem["_id"])},
        message="Correctly retrieved problem"
    )
