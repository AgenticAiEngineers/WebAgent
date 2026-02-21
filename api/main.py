from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from agent.agent_core import SimpleAgent
from memory.sqlite_memory import init_db

# create app FIRST
app = FastAPI()

# enable CORS (only once)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# initialize DB
init_db()

# agent instance
agent = SimpleAgent()

# request schema
class QueryRequest(BaseModel):
    query: str

# endpoint
@app.post("/chat")
def ask_agent(data: QueryRequest):
    response = agent.run(data.query)
    return {"response": response}