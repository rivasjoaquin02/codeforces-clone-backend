
from fastapi import FastAPI
from server.routes.auth import router as AuthRouter

app = FastAPI()
app.include_router(AuthRouter, tags=["Auth"])


@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to this fantastic app!"}
