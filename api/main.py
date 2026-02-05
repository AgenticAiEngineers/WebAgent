from fastapi import FastAPI
from pydantic import BaseModel
from agent.agent_core import SimpleAgent

app = FastAPI()

agent = SimpleAgent()


class QueryRequest(BaseModel):
    query: str


@app.post("/ask")
def ask_agent(data: QueryRequest):

    response = agent.run(data.query)

    return {
        "response": response
    }
