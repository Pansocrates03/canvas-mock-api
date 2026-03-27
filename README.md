# canvas-api-simulator
Simulates the CRUD API of LMS Canvas for development purposes.

## Run development server
1. Install the dependencies
```
pip install fastapi uvicorn
```

2. Run development server
```
uvicorn main:app --reload
```

3. Check the docs at `http://127.0.0.1:8000`

## Coberture

| Module | Coberture |
| ----- | ----- |
| assignments | medium |
| courses | medium |
| enrollments | medium |
| oauth | medium |
| quizzes | medium |