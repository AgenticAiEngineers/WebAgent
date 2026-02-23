from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from agent.agent_core import SimpleAgent
from orchestrator.executor import Executor
from memory.sqlite_memory import init_db

# create app FIRST
app = FastAPI()

# enable CORS (only once)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# initialize DB
init_db()

# agent instances
simple_agent = SimpleAgent()
executor_agent = Executor()

# request schema
class QueryRequest(BaseModel):
    query: str
    agent: str = "simple"

@app.get("/")
def health():
    return JSONResponse({"status": "ok", "message": "WebAgent API is running"})

@app.get("/agents")
def list_agents():
    return {"agents": ["simple", "executor"]}

# endpoint
@app.post("/chat")
def ask_agent(data: QueryRequest):
    agent_name = (data.agent or "simple").strip().lower()

    if agent_name == "executor":
        response = executor_agent.handle(data.query)
        return {"response": response, "agent": "executor"}

    response = simple_agent.run(data.query)
    return {"response": response, "agent": "simple"}
