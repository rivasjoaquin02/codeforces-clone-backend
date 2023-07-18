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

from app.models.problem_crud import retrieve_problems

# utils


problems_collection = client.problems.get_collection("problems_collection")
problems_inserted: list[dict] = []


def generate_n_problems_schema(n: int):
    # generate problems
    problems = [
        ProblemSchema(
            authorId=f"{i}",
            title=f"Foo Bar {i}",
            description="foo bar",
            example_input="foo bar",
            example_output="foo bar",
            tags=["foo", "bar"],
        )
        for i in range(n)
    ]

    return problems


async def fill_db(n: int):
    """
    add problems to DB for testing
    """
    # clean test_problem_collection
    # problems_collection.drop()

    # generate problems
    problems: list[ProblemSchema] = generate_n_problems_schema(n)
    for problem in problems:
        p: dict = await problems_collection.insert_one(problem.dict())
        problems_inserted.append(p)


async def clear_db():
    """
    remove problems added to DB for testing
    """
    for problem in problems_inserted:
        await problems_collection.delete_one({"_id": problem["_id"]})


def find_title_problems_inserted(title: str) -> bool:
    for problem in problems_inserted:
        if problem["title"] == title:
            return True
    return False


# TEST's


async def test_retrieve_problems():
    # add 10 problems
    await fill_db(10)

    problems = await retrieve_problems()
    for problem in problems:
        assert find_title_problems_inserted(problem.title)

        # remove 10 problems
    await clear_db()


async def retrieve_problem(field: str, key: str | ObjectId) -> ProblemDBSchema | None:
    problem_in_db = await problems_collection.find_one({field: key})

    if not problem_in_db:
        return None

    return dict_to_problem_db_schema(problem_in_db)


async def add_problem(problem_data: ProblemSchema) -> ProblemDBSchema | None:
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
        "authorId": problem_data.authorId,
        "title": problem_data.title,
        "description": problem_data.description,
        "example_input": problem_data.example_input,
        "example_output": problem_data.example_output,
        "tags": problem_data.tags,
    }

    inserted_id = await problems_collection.insert_one(problem_to_insert).inserted_id
    problem_in_db = await retrieve_problem("_id", inserted_id)
    return problem_in_db


async def update_problem(id: str, problem_data: UpdateProblemSchema) -> ProblemDBSchema:
    """
    Update a problem with matching ID
    """
    problem_in_db = await retrieve_problem("_id", ObjectId(id))
    if not problem_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Problem not found"
        )

    problem_to_update = {k: v for k, v in problem_data.dict().items() if v is not None}

    updated_problem = await problems_collection.update_one(
        {"_id": ObjectId(id)}, {"$set": problem_to_update}
    )

    if updated_problem.modified_count > 0:
        problem_in_db = await retrieve_problem("_id", ObjectId(id))
        if problem_in_db:
            return problem_in_db

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Error no new info to update..."
    )


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
    return dict_to_problem_db_schema(deleted_problem)
