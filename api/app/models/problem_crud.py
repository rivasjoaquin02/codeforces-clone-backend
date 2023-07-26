from fastapi import HTTPException, status

# db client
from app.db.database import client

# models
from app.models.problem import (
    ProblemDBSchema,
    ProblemSchema,
    UpdateProblemSchema,
    dict_to_problem_db_schema,
)

from bson import ObjectId

# utils


problems_collection = client.problems.get_collection("problems_collection")


async def retrieve_problems() -> list[ProblemDBSchema]:
    problems = []
    async for problem in problems_collection.find():
        problems.append(dict_to_problem_db_schema(problem))
    return problems


async def retrieve_problem(field: str, key: str | ObjectId) -> ProblemDBSchema | None:
    problem_in_db: dict = await problems_collection.find_one({field: key})

    if not problem_in_db:
        return None

    return dict_to_problem_db_schema(problem_in_db)


async def add_problem(authorId: str, problem_data: ProblemSchema) -> ProblemDBSchema:
    """
    Add a new problem to the DB
    """

    problem_in_db = await retrieve_problem("title", problem_data.title)

    if problem_in_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Problem Title already exist",
        )

    problem_to_insert = {
        "authorId": authorId,
        "title": problem_data.title,
        "description": problem_data.description,
        "example_input": problem_data.example_input,
        "example_output": problem_data.example_output,
        "tags": problem_data.tags,
    }

    inserted_problem = await problems_collection.insert_one(problem_to_insert)
    inserted_id: ObjectId = inserted_problem.inserted_id
    problem_in_db = await retrieve_problem("_id", inserted_id)

    if not problem_in_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Problem not added",
        )

    return problem_in_db


async def update_problem(
    id: str, authorId: str, problem_data: UpdateProblemSchema
) -> ProblemDBSchema:
    """
    Update a problem with matching ID
    """
    problem_in_db = await retrieve_problem("_id", ObjectId(id))
    if not problem_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Problem not found"
        )

    if not problem_in_db.authorId == authorId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are not the author of this problem, you can't edit it",
        )

    problem_to_update = {k: v for k, v in problem_data.dict().items() if v is not None}

    updated_problem = await problems_collection.update_one(
        {"_id": ObjectId(id)}, {"$set": problem_to_update}
    )

    if updated_problem.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Error no new info to update...",
        )

    problem_in_db = await retrieve_problem("_id", ObjectId(id))
    if not problem_in_db:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Error while updating...",
        )

    return problem_in_db


async def delete_problem(id: str) -> ProblemSchema:
    """
    Delete a problem with a matching ID
    """

    problem_in_db = await retrieve_problem("_id", ObjectId(id))
    if not problem_in_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Problem not found"
        )

    deleted_problem = await problems_collection.delete_one({"_id": ObjectId(id)})

    if not deleted_problem:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Problem not deleted"
        )

    return problem_in_db
