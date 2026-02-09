import json
import time
from groq import Groq
from app.config import GROQ_API_KEY, MODEL_NAME, MAX_TURNS
from app.tools import TOOLS
from app.memory import memory

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """
You are an Agentic AI Task Orchestrator.

Rules:
- For research/facts → use search tool.
- Do NOT invent APIs.
- Do NOT use code for web calls.
- After 1–2 searches, STOP and return final.

Return ONLY valid JSON.
Schema:
{
  "thought": "...",
  "action": "search:<query> | calc:<expr> | code:<python> | final:<answer>"
}
"""

def extract_first_json(text: str):
    text = text.strip().replace("```", "")
    start = text.find("{")
    if start == -1:
        raise ValueError("No JSON start found")

    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return json.loads(text[start:i+1])

    raise ValueError("No complete JSON object found")

def call_llm_with_retry(messages, retries=1):
    for attempt in range(retries + 1):
        try:
            return client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                temperature=0.2,
                timeout=30
            )
        except Exception as e:
            if attempt == retries:
                raise
            time.sleep(1.5)

def run_agent(task: str):
    steps = []
    memory.add(task)
    context = []

    for _ in range(MAX_TURNS):
        try:
            resp = call_llm_with_retry([
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Task: {task}\nSteps: {steps}\nContext: {context}"}
            ], retries=1)

            raw = resp.choices[0].message.content
            data = extract_first_json(raw)

            thought = str(data.get("thought", ""))
            action = str(data.get("action", ""))

            if action.startswith("final:"):
                return {"result": action.replace("final:", "").strip(), "steps": steps}

            tool_name, tool_input = action.split(":", 1)
            tool_fn = TOOLS.get(tool_name.strip())

            observation = tool_fn(tool_input.strip()) if tool_fn else "Unknown tool"

            steps.append({
                "thought": thought,
                "action": action,
                "observation": str(observation)
            })

            if tool_name.strip() == "search":
                context.append(str(observation))

        except Exception as e:
            steps.append({
                "thought": "Provider error",
                "action": "retry",
                "observation": str(e)
            })
            # continue loop

    # Fallback: summarize from whatever we have
    if context:
        try:
            final_resp = call_llm_with_retry([
                {"role": "user", "content": f"Summarize the answer for: {task}\nContext: {context}"}
            ], retries=1)
            return {"result": final_resp.choices[0].message.content.strip(), "steps": steps}
        except Exception:
            pass

    return {
        "result": "Unable to complete task due to provider connectivity issues. Please try again.",
        "steps": steps
    }
