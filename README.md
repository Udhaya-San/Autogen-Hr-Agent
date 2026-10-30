# AutoGen HR Assistant Agent

Week 5 · Day 1 assignment: a single AutoGen `AssistantAgent` with the system message
**"You are an HR assistant."** that writes a 5-line job description for any role.

## What it does

1. Asks which role you want (press Enter for the default, *Junior Python Developer*).
2. Sends the task to the agent through an OpenAI model (`gpt-4o-mini`).
3. Streams back exactly 5 numbered lines, one short sentence each, covering:
   responsibilities, required skills, tools, teamwork and growth.

## Why the prompt is written this way

"Write 5 lines" is ambiguous: a model may return 5 paragraphs, 5 sentences, or a title plus
5 bullets. The task spells out the format (exactly 5 numbered lines, no title, no intro,
no closing remarks), so the output is predictable and easy to check.

## Project structure

```
.
├── hr_agent.py        # the agent
├── requirements.txt   # dependencies
├── .env.example       # template for your API key
├── .gitignore         # keeps .env and venv/ out of Git
└── README.md
```

## Setup

You need Python 3.10 to 3.12 and an OpenAI API key.

**Windows (PowerShell)**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```
If PowerShell blocks the script, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first.

**macOS / Linux**
```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

**API key:** copy `.env.example` to `.env` and put your key in it:
```
OPENAI_API_KEY=your_openai_api_key_here
```
The key is read from the environment and is never hard-coded. `.env` is listed in
`.gitignore`, so it is not pushed to GitHub.

## Run

```bash
python hr_agent.py
```
Type a role such as `Software Tester`, or press Enter for the default.

## Sample output

Paste your own terminal output here after you run it, for example:

```
Which role? (press Enter for Junior Python Developer):
---------- TextMessage (user) ----------
Write a job description for a Junior Python Developer. ...
---------- TextMessage (hr_assistant) ----------
1. ...
2. ...
3. ...
4. ...
5. ...
```

## How it works

- `OpenAIChatCompletionClient` connects to the model.
- `AssistantAgent` carries the system message and the model client.
- `Console(agent.run_stream(task=...))` streams the reply to the terminal.
- `model_client.close()` runs in a `finally` block. Without it the script can hang after
  finishing because the connection pool is still open.

## Troubleshooting

| Problem | Cause | Fix |
| :-- | :-- | :-- |
| `OPENAI_API_KEY is not set` | `.env` missing, or run from another folder | Create `.env` in the same folder as `hr_agent.py` and run from there |
| `ModuleNotFoundError: autogen_agentchat` | Packages not installed in the active venv | Activate the venv, then `python -m pip install -r requirements.txt` |
| Script hangs at the end | Client not closed | Keep `await model_client.close()` in `finally` |
| Reply has a title or extra text | Prompt too loose | Keep the exact-format instruction in `build_task` |
