from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from gradescopeapi.classes.connection import GSConnection

LIMIT = 50

app = FastAPI(
    title="Better Gradescope API",
    description="API for Better Gradescope",
    version="0.1.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to Better Gradescope API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/courses")
async def get_items(email: str, password: str):
    connection = GSConnection()
    connection.login(email, password)
    courses = connection.account.get_courses().get("student", {})
    course_ids = list(courses.keys())

    assignments = []
    for course_id in course_ids:
        course_assigments = connection.account.get_assignments(course_id)
        assignments.extend(course_assigments)

    assignments = [a for a in assignments if a.due_date is not None]
    assignments.sort(key=lambda c: c.due_date, reverse=True)

    return {"assignments": assignments[:LIMIT]}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
