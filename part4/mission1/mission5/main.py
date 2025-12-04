from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from domain.question import question_router

app = FastAPI()

# CORS configuration (optional but good practice)
origins = [
    "http://localhost:5173",  # Vue.js default port, adjust if needed
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(question_router.router)

@app.get("/")
def read_root():
    return {"message": "Hello World"}
