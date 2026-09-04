from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def get():
    return {"message": "Job Application Tracker API"}


