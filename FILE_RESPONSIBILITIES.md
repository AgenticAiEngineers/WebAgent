# File Responsibilities and Requirements

## 1. Agent Layer (`agent/`)

### `agent/agent_core.py`
- Responsibility: Main multi-step agent runtime (`SimpleAgent`) with context building, tool execution, planning, reflection, and memory writes.
- Needs:
  - `LLMClient`
  - tool functions (`calculator_tool`, `search_tool`, `smart_query_rewrite`, `time_tool`)
  - memory modules (`sqlite_memory`, `chromadb_memory`)
  - `PlannerAgent`, `ReflectionAgent`

### `agent/planner_agent.py`
- Responsibility: Creates search plans (`create_plan`) and task plans (`create_task_plan`) using LLM.
- Needs: `LLMClient`.

### `agent/reflection_agent.py`
- Responsibility: Reviews generated answers, returns corrections, appends lessons to `memory/learning_log.txt`.
- Needs: `LLMClient`, writable `memory/learning_log.txt`.

### `agent/research_agent.py`
- Responsibility: Runs web search and summarizes findings for task research.
- Needs: `LLMClient`, `tools/web_tool.py`.

### `agent/tools.py`
- Responsibility: Local tool wrappers for calculator, web search, time formatting, and query rewrite.
- Needs:
  - `ddgs` or `duckduckgo_search` package
  - `requests` for time API call.

### `agent/validator_agent.py`
- Responsibility: Safety/content validator pass over final drafts.
- Needs: `LLMClient`.

### `agent/writer_agent.py`
- Responsibility: Converts plan + research data into final structured content.
- Needs: `LLMClient`.

## 2. API Layer (`api/`)

### `api/main.py`
- Responsibility: FastAPI app setup, CORS, `/chat` endpoint with agent selection, `/agents` list endpoint, root health endpoint, startup memory init.
- Needs:
  - FastAPI + Pydantic
  - `SimpleAgent`
  - `Executor`
  - `init_db()` from memory layer.

## 3. Frontend (`frontend/`)

### `frontend/index.html`
- Responsibility: React entry HTML for Vite app mount.

### `frontend/src/main.jsx`
- Responsibility: React bootstrap entrypoint.

### `frontend/src/App.jsx`
- Responsibility: Main UI, message rendering, API calls, agent selector (`simple` / `executor`).

### `frontend/src/styles.css`
- Responsibility: UI styling and responsive layout.

## 4. LLM Layer (`llm/`)

### `llm/llm_client.py`
- Responsibility: Unified model client wrapper; handles Gemini SDK imports and text generation.
- Needs:
  - `.env` API key
  - one supported SDK (`google-genai` or `google-generativeai`).

## 5. Memory Layer (`memory/`)

### `memory/chromadb_memory.py`
- Responsibility: Vector memory store and semantic retrieval.
- Needs:
  - `chromadb`
  - `sentence-transformers`
  - falls back to in-process list if unavailable.

### `memory/learning_log.txt`
- Responsibility: Reflection lessons log file.
- Needs: write access.

### `memory/memory_classifier.py`
- Responsibility: Decide if user input should be stored as memory.
- Current state: Placeholder (`return True` for all input).
- Suggested need: real classifier logic (rule-based or LLM-based).

### `memory/retriever.py`
- Responsibility: Filters relevant memories for current query using LLM.
- Needs: `LLMClient` passed from caller.

### `memory/sqlite_memory.py`
- Responsibility: Persistent chat history storage and retrieval.
- Needs:
  - `sqlite3` module (if available),
  - otherwise uses JSON fallback (`memory/storage.json` list format).

### `memory/storage.json`
- Responsibility:
  - file tool key-value storage in `tools/file_tool.py`,
  - JSON fallback message storage in `memory/sqlite_memory.py` (list format).
- Note: used by multiple modules with different JSON structures.

## 6. Orchestrator Layer (`orchestrator/`)

### `orchestrator/executor.py`
- Responsibility: Intent-based execution engine using `Router`; invokes calculator, memory, web, planner pipeline, and memory-aware LLM flow.
- Needs:
  - all agent classes
  - router
  - memory modules
  - calculator/web tools.

### `orchestrator/router.py`
- Responsibility: LLM-powered intent classification (`calculator`, `memory`, `web_tool`, `planner`, `llm`).
- Needs: `LLMClient` instance passed in.

## 7. Tools Layer (`tools/`)

### `tools/calculator_tool.py`
- Responsibility: Safe-ish calculator wrapper (currently `eval` based).
- Needs: input sanitation improvements for production safety.

### `tools/file_tool.py`
- Responsibility: Save/get key-value memory to/from `memory/storage.json`.
- Needs: JSON file read/write access.

### `tools/time_tool.py`
- Responsibility: Local date/time formatting utility.
- Note: function exposed is `time_tool()`.

### `tools/web_tool.py`
- Responsibility: DuckDuckGo search wrapper using `ddgs` with fallback to `duckduckgo_search`.
- Needs:
  - `ddgs` or `duckduckgo-search`.

## 8. Entrypoints and Tests (Root)

### `docker/docker-compose.yml`
- Responsibility: Runs backend + React frontend containers together.

### `docker/backend/Dockerfile`
- Responsibility: Backend container build and runtime.

### `docker/frontend/Dockerfile`
- Responsibility: Frontend container build (Node build + Nginx runtime).

### `docker/frontend/nginx.conf`
- Responsibility: SPA routing fallback to `index.html`.

### `main.py`
- Responsibility: CLI chat loop using `SimpleAgent`.
- Needs: full agent stack and valid API key.

### `test_time.py`
- Responsibility: quick manual test for time tool.
- Current issue: imports `get_live_time` which is not defined in `tools/time_tool.py`.

### `test_executor.py`
- Responsibility: manual interactive test loop for `Executor`.

### `test_calculator.py`
- Responsibility: manual interactive test loop for calculator tool.

## 9. Suggested Priorities
1. Fix `test_time.py` import mismatch (`get_live_time` vs `time_tool`).
2. Separate `memory/storage.json` usage by purpose (or split into two files).
3. Replace raw `eval` usage in calculator code with safer parsing.
4. Implement real logic in `memory/memory_classifier.py`.
