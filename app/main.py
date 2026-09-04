from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, field_validator
from enum import Enum

app = FastAPI()

class JobStatus(str, Enum):
    APPLIED = "applied"
    SCREENING = "screening"
    INTERVIEW = "interview"
    OFFER = "offer"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"
    Active = "active"

jobs = [{
    "id" : 1,
    "company" : "ABC",
    "position" : "Analyst",
    "location" : "India",
    "status" : "Active",
    "notes" : "any-comments" 
}]

class Jobs(BaseModel):
    company: str = Field(min_length=2, max_length=100)
    position: str = Field(min_length=2, max_length=100)
    location: str = Field(min_length=2, max_length=100)
    status: JobStatus
    notes: str = Field(min_length=1, max_length=500)
    @field_validator("company", "position", "location", "notes")
    @classmethod
    def remove_whitespace(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("Value cannot be empty")
        return value



@app.get("/")
def get():
    return {"message": "Job Application Tracker API"}

@app.post("/create-jobs", status_code=status.HTTP_201_CREATED)
def create_jobs(jb: Jobs):
    new_id = len(jobs)+1
    new_job = {
        "id" : new_id,
        "company" : jb.company,
        "position": jb.position,
        "location" : jb.location,
        "status" : jb.status,
        "notes" : jb.notes
        }
    jobs.append(new_job)
    return new_job  

@app.get("/jobs",status_code=status.HTTP_200_OK)
def get_all_jobs():
    return jobs

@app.get("/jobs/{job_id}", status_code=status.HTTP_200_OK)
def get_specific_job(job_id: int):
    for jb in jobs:
        if jb["id"] == job_id:
            return jb
    raise HTTPException(status_code=404, detail="Job Not Found")

@app.get("/jobs", status_code=status.HTTP_200_OK)
def get_jobs(status: JobStatus | None = None, company: str | None = None, location: str |None = None):
    filtered_jobs = []
    for jb in jobs:
        if status is not None and jb["status"] != status:
            continue

        if company is not None and jb["company"] != company:
            continue

        if location is not None and jb["location"] != location:
            continue

        filtered_jobs.append(jb)
    return filtered_jobs

@app.get("/jobs/search")
def job_search(query: str):
    result = []
    for jb in jobs:
        if (query.lower() in jb["company"].lower() or query.lower() in jb["position"].lower() or query.lower() in jb["notes"].lower()):
            result.append(jb)
    return result


@app.put("/jobs-update/{job_id}", status_code=status.HTTP_200_OK)
def update_job(job_id: int, jb: Jobs):
    for j in jobs:
        if j["id"] == job_id:
            j["company"] = jb.company
            j["position"] = jb.position
            j["location"] = jb.location
            j["status"] = jb.status
            j["notes"] = jb.notes
            return j
    raise HTTPException(status_code=404,
                        detail="Job Not Found")

@app.delete("/jobs/{job_id}",status_code=status.HTTP_200_OK)
def delete_job(job_id:int):
    for j in jobs:
        if j["id"] == job_id:
            jobs.remove(j)
            return {"message": "Job deleted successfully"}
    raise HTTPException(status_code=404,
                        detail="Job Not Found")





