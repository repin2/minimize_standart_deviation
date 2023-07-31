from fastapi import FastAPI

from api import minimize_router

app = FastAPI()
app.include_router(minimize_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app")
