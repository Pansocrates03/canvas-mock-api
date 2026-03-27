from fastapi import FastAPI
from modules.courses import router as courses_router
from modules.assignments import router as assignments_router
from modules.quizzes import router as quizzes_router
from modules.enrollments import router as enrollments_router

app = FastAPI(
    title="Canvas Mock API",
    description="API simulada de Canvas estructurada por módulos.",
    version="1.0.0"
)

# Registrar los módulos
app.include_router(courses_router.router)
app.include_router(assignments_router.router)
app.include_router(quizzes_router.router)
app.include_router(enrollments_router.router)

@app.get("/")
async def root():
    return {"message": "El Canvas Mock API modularizado está funcionando correctamente."}