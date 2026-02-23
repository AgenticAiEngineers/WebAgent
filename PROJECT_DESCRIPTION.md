# WebAgent Project Description

## 1. Project Agenda
This project builds a multi-agent AI assistant that can:
- accept user queries through a FastAPI backend and simple web UI,
- decide how to solve a query (tool usage vs direct LLM response),
- run utility tools (calculator, web search, time),
- keep conversation memory,
- generate and refine answers through specialized agent roles.

The main agenda is to create a practical "agentic" workflow instead of a single prompt-response model.

## 2. What This Project Can Do
- Chat with users through API (`POST /chat`) and browser UI.
- Route requests by intent (math, memory, web, planner, general LLM).
- Perform calculations from user input.
- Run DuckDuckGo-based web search for research tasks.
- Generate task plans and multi-step responses.
- Produce long-form writing with planner + research + writer + validator pipeline.
- Store and retrieve memory (SQLite when available, JSON fallback in current code).
- Run reflection/review steps to improve answer quality.

## 3. Core Architecture
- `api/main.py`: FastAPI app entrypoint, CORS, route definitions, app wiring.
- `agent/`: role-based agents (planner, researcher, writer, validator, reflection, core flow).
- `orchestrator/`: router/executor flow for intent-based execution path.
- `memory/`: chat memory, retrieval, vector memory layer, learning logs.
- `tools/`: utility tools (web, calculator, time, file helpers).
- `llm/`: model client wrapper for Gemini SDK usage.
- `frontend/`: React (JavaScript) frontend with agent selector UI.
- `docker/`: all Docker configuration files (compose + backend/frontend images).

## 4. End-to-End Flow (High Level)
1. User sends input from UI/CLI.
2. Backend accepts request in `/chat`.
3. Agent/orchestrator decides best path:
   - direct tool call,
   - planner/research/writer pipeline,
   - memory-aware LLM response.
4. Output is optionally validated/reflected.
5. Response is saved to memory and returned to user.

## 5. Runtime Requirements
- Python virtual environment.
- Dependencies from `requirements.txt`.
- Gemini API key in `.env` (current code accepts `GOOGLE_API_KEY`, `GEMINI_API_KEY`, or `OPENAI_API_KEY` as fallback key names).
- Uvicorn/FastAPI runtime.
- Docker + Docker Compose (for containerized run).

## 6. Current Limitations / Notes
- `test_time.py` references `get_live_time()` which does not exist in current `tools/time_tool.py`.
- `memory/memory_classifier.py` currently returns `True` for all inputs (placeholder behavior).
- `memory/learning_log.txt` can grow over time; no rotation is implemented.

## 7. Main Use Cases
- Personal AI assistant with lightweight memory.
- Research + summarization assistant.
- Blog/article drafting assistant using planner pipeline.
- Tool-augmented conversational bot for demos and learning agentic patterns.
