from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.auth import router as AuthRouter
from app.routes.users import router as UsersRouter
from app.routes.problems import router as ProblemsRouter

app = FastAPI()
app.include_router(AuthRouter, tags=["Auth"], prefix="/auth")
app.include_router(UsersRouter, tags=["Users"], prefix="/users")
app.include_router(ProblemsRouter, tags=["Problems"], prefix="/problems")

# CROSS (Cross-Origin RESOURCE SHARING)
origins = ["http://localhost", "http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*", "Content-Type", "Authorization"],
)


@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to this fantastic app!"}
