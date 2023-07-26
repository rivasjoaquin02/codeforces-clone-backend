# BEGIN: 8d5b6f7g3hj4
from bson import ObjectId
from fastapi import HTTPException, status
from app.models.problem import ProblemDBSchema, UpdateProblemSchema
from app.tests.utils.utils import random_problem, random_problem_dict


async def test_add_problem(test_app, test_database):
    problem_data = random_problem_dict()
    response = await test_app.post("/problems/", json=problem_data)
    assert response.status_code == status.HTTP_201_CREATED

    problem = await test_database["problems"].find_one({"_id": response.json()["_id"]})
    assert problem is not None
    assert problem["title"] == problem_data["title"]


async def test_add_problem_existing_title(test_app, test_database):
    problem_data = random_problem_dict()
    await test_database["problems"].insert_one(problem_data)

    response = await test_app.post("/problems/", json=problem_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


async def test_retrieve_problem(test_app, test_database):
    problem_data = random_problem_dict()
    problem = ProblemDBSchema(**problem_data)
    await test_database["problems"].insert_one(problem.dict())

    response = await test_app.get(f"/problems/{problem.id}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == problem_data["title"]


async def test_retrieve_problem_incorrect_id(test_app, test_database):
    response = await test_app.get("/problems/123/")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_retrieve_problem_not_found(test_app, test_database):
    response = await test_app.get(f"/problems/{str(ObjectId())}/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_retrieve_problems(test_app, test_database):
    problem_data = random_problem_dict()
    problem = ProblemDBSchema(**problem_data)
    await test_database["problems"].insert_one(problem.dict())

    response = await test_app.get("/problems/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == problem_data["title"]


async def test_update_problem(test_app, test_database):
    problem_data = random_problem_dict()
    problem = ProblemDBSchema(**problem_data)
    await test_database["problems"].insert_one(problem.dict())

    problem_update = UpdateProblemSchema(title="New Title")
    response = await test_app.put(
        f"/problems/{problem.id}/", json=problem_update.dict()
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "New Title"


async def test_update_problem_not_found(test_app, test_database):
    problem_update = UpdateProblemSchema(title="New Title")
    response = await test_app.put(
        f"/problems/{str(ObjectId())}/", json=problem_update.dict()
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_update_problem_no_new_info(test_app, test_database):
    problem_data = random_problem_dict()
    problem = ProblemDBSchema(**problem_data)
    await test_database["problems"].insert_one(problem.dict())

    problem_update = UpdateProblemSchema()
    response = await test_app.put(
        f"/problems/{problem.id}/", json=problem_update.dict()
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


async def test_delete_problem(test_app, test_database):
    problem_data = random_problem_dict()
    problem = ProblemDBSchema(**problem_data)
    await test_database["problems"].insert_one(problem.dict())

    response = await test_app.delete(f"/problems/{problem.id}/")
    assert response.status_code == status.HTTP_200_OK

    problem_in_db = await test_database["problems"].find_one({"_id": problem.id})
    assert problem_in_db is None


async def test_delete_problem_not_found(test_app, test_database):
    response = await test_app.delete(f"/problems/{str(ObjectId())}/")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


# END: 8d5b6f7g3hj4
