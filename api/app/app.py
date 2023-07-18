from fastapi import FastAPI
from app.routes.auth import router as AuthRouter
from app.routes.users import router as UsersRouter
from app.routes.problems import router as ProblemsRouter

app = FastAPI()
app.include_router(AuthRouter, tags=["Auth"], prefix="/auth")
app.include_router(UsersRouter, tags=["Users"], prefix="/users")
app.include_router(ProblemsRouter, tags=["Problems"], prefix="/problems")


@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to this fantastic app!"}
