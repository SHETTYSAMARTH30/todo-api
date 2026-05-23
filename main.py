from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Todo API")

todos: dict[int, dict] = {}
_next_id = 1


class TodoIn(BaseModel):
    title: str
    done: bool = False


class TodoOut(BaseModel):
    id: int
    title: str
    done: bool


@app.get("/todos", response_model=list[TodoOut])
def list_todos():
    return [{"id": k, **v} for k, v in todos.items()]


@app.post("/todos", response_model=TodoOut, status_code=201)
def create_todo(todo: TodoIn):
    global _next_id
    todos[_next_id] = {"title": todo.title, "done": todo.done}
    out = {"id": _next_id, **todos[_next_id]}
    _next_id += 1
    return out


@app.get("/todos/{todo_id}", response_model=TodoOut)
def get_todo(todo_id: int):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"id": todo_id, **todos[todo_id]}


@app.put("/todos/{todo_id}", response_model=TodoOut)
def update_todo(todo_id: int, todo: TodoIn):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    todos[todo_id] = {"title": todo.title, "done": todo.done}
    return {"id": todo_id, **todos[todo_id]}


@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    del todos[todo_id]
