

from bson import ObjectId
from server.db.models.problem import ProblemSchema
from server.db.database import client


problems_collection = client.problems.get_collection("problems_collection")


# CRUD

async def retrieve_problems() -> list:
    problems = []
    async for problem in problems_collection.find():
        problems.append({**problem, "_id": str(problem["_id"])})
    return problems


async def retrieve_problem(field: str, key: str | ObjectId) -> dict | None:
    return await problems_collection.find_one({field: key})


async def add_problem(problem_data: ProblemSchema) -> dict | None:
    '''
    Add a new problem to the DB
    '''
    exist = await retrieve_problem("title", problem_data.title)

    if not exist:
        plain_problem_data = {
            "authorId": problem_data.authorId,
            "title": problem_data.title,
            "description": problem_data.description,
            "example_input": problem_data.example_input,
            "example_output": problem_data.example_output,
            "tags": problem_data.tags,
        }
        print(plain_problem_data)
        problem = await problems_collection.insert_one(plain_problem_data)
        inserted_problem = await retrieve_problem("_id", problem.inserted_id)
        return {**inserted_problem, "_id": str(inserted_problem["_id"])}
