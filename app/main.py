from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path
from app.agent import run_agent

app = FastAPI(title="Agentic AI Task Orchestrator")

BASE_DIR = Path(__file__).resolve().parent.parent

@app.get("/")
def root():
    ui_path = BASE_DIR / "ui" / "index.html"
    if ui_path.exists():
        return FileResponse(ui_path)
    return JSONResponse(
        status_code=404,
        content={"error": "UI not found. Make sure ui/index.html exists."}
    )

@app.post("/run")
def run_task(body: dict):
    try:
        task = body.get("task", "")
        if not task:
            return {"result": "Missing 'task' in request body.", "steps": []}

        out = run_agent(task)

        # Force schema-safe output
        result = out.get("result", "")
        steps = out.get("steps", [])

        safe_steps = []
        for s in steps:
            safe_steps.append({
                "thought": str(s.get("thought", "")),
                "action": str(s.get("action", "")),
                "observation": str(s.get("observation", ""))
            })

        return {
            "result": result,
            "steps": safe_steps
        }
    except Exception as e:
        return {
            "result": f"Error: {str(e)}",
            "steps": []
        }
