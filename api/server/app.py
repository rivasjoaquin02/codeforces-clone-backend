
from fastapi import FastAPI
from server.routes.auth import router as AuthRouter
from server.routes.problems import router as ProblemsRouter

app = FastAPI()
app.include_router(AuthRouter, tags=["Auth"])
app.include_router(ProblemsRouter, tags=["Problems"])


@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to this fantastic app!"}
