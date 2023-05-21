# gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
# uvicorn main:app --reload
from fastapi import FastAPI
from router import agent_router, completion_router, image_router, user_router
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,  # This is required
        allow_methods=["*"],
        allow_headers=["*"],
    )
]
app = FastAPI(middleware=middleware)
app.include_router(agent_router.router)
app.include_router(completion_router.router)
app.include_router(image_router.router)
app.include_router(user_router.router)


@app.get("/")
def health_check():
    return "Server is up!"
