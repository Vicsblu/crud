from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

tasks=[
    {"id":1, "title":"Learn FastAPI","done": False},
    {"id":2, "title":"Finish FlyRank Assignment","done": False},
    {"id":3, "title": "Push project to Github","done": False},
]
class TaskCreate(BaseModel):
    title: str
    
class TaskUpdate(BaseModel):
    title: str
    done: bool
    
@app.get("/")
def root():
    return {
            "name":"Task API",
            "version": "1.0",
            "endpoints":["/tasks"]
    }
@app.get("/health")
def health():
    return{
        "status":"ok"
    }
    
@app.get("/tasks")
def get_task():
    return tasks 
    
@app.get("/tasks/{id}")
def get_task(id:int):
    for task in tasks:
        if task["id"]==id:
            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task{id} not found"
    )
    
@app.post("/tasks",status_code=201)
def create_task(task:TaskCreate):
    new_task= {
        "id":len(tasks) + 1,
        "title":task.title,
        "done":False
    }
    tasks.append(new_task)
    
    return new_task

@app.put("/tasks/{id}")
def update_task(id:int,update:TaskUpdate):
    for task in tasks:
        if task["id"]==id:
            task["title"] = update.title
            task["done"] = update.done
            return task
    raise HTTPException(
        status_code=404,
        detail=f"Task{id} not found"
    )
@app.delete("/tasks/{id}")
def delete_task(id: int):
    for task in tasks:
        if task["id"] == id:
            tasks.remove(task)
            return {"message":f"Task{id} Deleted Successfully"}
    raise HTTPException(
        status_code=404,
        detail=f"Task{id} not found"
    )