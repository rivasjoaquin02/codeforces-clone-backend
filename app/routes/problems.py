from fastapi import APIRouter, Body, Depends, HTTPException, status
from app.dependencies import current_active_user

from app.models.problem import ProblemSchema, ProblemDBSchema, UpdateProblemSchema
from app.models.problem_crud import (
    add_problem,
    retrieve_problem,
    retrieve_problems,
    update_problem,
    delete_problem,
)
from app.models.solution import SolutionResultSchema, SolutionSchema
from app.models.user import UserSchema

from bson import ObjectId

from app.service.submit_solution import submit_solution

router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_description="Retrieves all problems",
    response_model=list[ProblemDBSchema],
)
async def get_problems():
    problem_list = await retrieve_problems()
    if len(problem_list) == 0:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, detail="No problems to retrieve yet"
        )

    return problem_list


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_description="Retrieves problem with matching ID",
    response_model=ProblemDBSchema,
)
async def get_problem(id: str):
    problem_in_db = await retrieve_problem("_id", ObjectId(id))
    if not problem_in_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No problem with that id"
        )

    return problem_in_db


@router.post(
    "/create",
    status_code=status.HTTP_200_OK,
    response_description="Insert new problem",
    response_model=ProblemDBSchema,
)
async def add_problem_data(
    problem_data: ProblemSchema = Body(...),
    user: UserSchema = Depends(current_active_user),
):
    print (problem_data)
    
    inserted_problem = await add_problem(user.id, problem_data)
    if not inserted_problem:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Problem not added",
        )

    return inserted_problem


@router.post(
    "/{id}/submit",
    status_code=status.HTTP_200_OK,
    response_description="Submit solution to problem with matching ID",
    response_model=SolutionResultSchema,
)
async def submit_problem_data(
    id: str, solution: SolutionSchema, user: UserSchema = Depends(current_active_user)
):
    problem = await retrieve_problem("_id", ObjectId(id))
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No problem with that id"
        )

    solution_result = await submit_solution(solution, problem)

    return solution_result


@router.put(
    "/{id}",
    status_code=status.HTTP_206_PARTIAL_CONTENT,
    response_description="Updates the problem info",
    response_model=ProblemDBSchema,
)
async def update_problem_data(
    id: str,
    problem_data: UpdateProblemSchema,
    user: UserSchema = Depends(current_active_user),
):
    updated_problem = await update_problem(id, user.id, problem_data)
    if not updated_problem:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not update problem info",
        )

    return updated_problem


@router.delete(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_description="Deletes the problem with matching ID",
    response_model=ProblemDBSchema,
)
async def delete_problem_data(id: str, user: UserSchema = Depends(current_active_user)):
    problem_in_db = await retrieve_problem("_id", ObjectId(id))
    if not problem_in_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No problem with that id"
        )

    if not problem_in_db.authorId == user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are not the author of this problem, you can't edit it",
        )

    deleted_problem = await delete_problem(id)
    if not deleted_problem:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Could not delete problem"
        )
    return deleted_problem
