from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Action(BaseModel):
    action: Any

INITIAL_STATE = {"battery": 50, "step": 0}
state = INITIAL_STATE.copy()

@app.post("/reset")
def reset():
    global state
    state = INITIAL_STATE.copy()
    return {"state": state}

@app.post("/step")
def step(action: Action):
    global state
    act = str(action.action)

    if act == "move":
        state["battery"] -= 10
    elif act == "charge":
        state["battery"] += 10

    state["step"] += 1
    state["battery"] = max(0, min(100, state["battery"]))
    reward = 1 if state["battery"] > 0 else 0
    done = state["battery"] == 0
    return {"state": state, "reward": reward, "done": done}
