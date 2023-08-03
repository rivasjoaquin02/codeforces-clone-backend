from app.models.problem import ProblemDBSchema, ProblemSchema, UpdateProblemSchema


def test_problem_schema():
    data = {
        "authorId": "1",
        "title": "Rudolph and Cut the Rope",
        "description": "There are nnails driven into the wall, the ith nail is drive...",
        "inputExample": "4 3 4 3 3 1 1 2",
        "outputExample": "2 2 3 0",
        "tags": ["implementation", "math"],
    }
    problem = ProblemSchema(**data)
    assert problem.authorId == data["authorId"]
    assert problem.title == data["title"]
    assert problem.description == data["description"]
    assert problem.inputExample == data["inputExample"]
    assert problem.outputExample == data["outputExample"]
    assert problem.tags == data["tags"]


def test_problem_db_schema():
    data = {
        "id": "123",
        "authorId": "456",
        "title": "Rudolph and Cut the Rope",
        "description": "There are nnails driven into the wall, the ith nail is drive...",
        "inputExample": "4 3 4 3 3 1 1 2",
        "outputExample": "2 2 3 0",
        "tags": ["implementation", "math"],
    }
    problem = ProblemDBSchema(**data)
    assert problem.id == data["id"]
    assert problem.authorId == data["authorId"]
    assert problem.title == data["title"]
    assert problem.description == data["description"]
    assert problem.inputExample == data["inputExample"]
    assert problem.outputExample == data["outputExample"]
    assert problem.tags == data["tags"]


def test_update_problem_schema():
    data = {
        "title": "Rudolph and Cut the Rope",
        "description": "There are nnails driven into the wall, the ith nail is drive...",
        "inputExample": "4 3 4 3 3 1 1 2",
        "outputExample": "2 2 3 0",
        "tags": ["implementation", "math"],
    }
    problem = UpdateProblemSchema(**data)
    assert problem.title == data["title"]
    assert problem.description == data["description"]
    assert problem.inputExample == data["inputExample"]
    assert problem.outputExample == data["outputExample"]
    assert problem.tags == data["tags"]


# helpers


def dict_to_problem_db_schema(problem: dict) -> ProblemDBSchema:
    return ProblemDBSchema(
        id=problem["_id"],
        authorId=problem["authorId"],
        title=problem["title"],
        description=problem["description"],
        inputExample=problem["inputExample"],
        outputExample=problem["outputExample"],
        tags=problem["tags"],
    )
