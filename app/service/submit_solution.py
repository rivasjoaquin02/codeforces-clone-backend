from app.models.problem import ProblemSchema
from app.models.solution import SolutionResultSchema, SolutionSchema, status_code


solution_stack: list[SolutionSchema] = []


async def submit_solution(
    solution: SolutionSchema, problem: ProblemSchema
) -> SolutionResultSchema:
    # add the solution to the stack
    solution_stack.append(solution)

    # wait for the solution to be processed
    return SolutionResultSchema(
        status=status_code.AC,
        run_time=0.001,
        memory=100,
    )