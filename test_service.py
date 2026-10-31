"""
test_service.py - A basic FastAPI server.

Install dependencies:
    pip install fastapi uvicorn

Run:
    python test_service.py
    # or
    uvicorn test_service:app --reload

Then open:
    http://127.0.0.1:8000/        -> welcome message
    http://127.0.0.1:8000/docs    -> interactive Swagger UI
"""

from typing import Dict, Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Test Service", version="1.0.0")


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float


# Simple in-memory store (resets when the server restarts)
items: Dict[int, Item] = {}
next_id = 1


@app.get("/")
def root():
    return {"message": "Test service is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/items")
def list_items():
    return items


@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]


@app.post("/items", status_code=201)
def create_item(item: Item):
    global next_id
    item_id = next_id
    items[item_id] = item
    next_id += 1
    return {"id": item_id, "item": item}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    items[item_id] = item
    return {"id": item_id, "item": item}


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    del items[item_id]
    return {"deleted": item_id}


if __name__ == "__main__":
    uvicorn.run("test_service:app", host="127.0.0.1", port=8000, reload=True)
