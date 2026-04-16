# PackageUpdateSearch Documentation

## Overview

PackageUpdateSearch is a Python CLI and agentic system that fetches, processes, and summarizes Reddit posts using the ReleaseTrain API. 
It supports both a command-line interface and an AI-powered agent (via Ollama:llama3.2:3b) that can call approved Python functions as tools and summarize results.

The system is designed around a controlled tool-execution architecture where all LLM actions are restricted to a predefined function registry.

---

## Core Features

### Reddit Data Fetching

The main function of the system is:

Update.package_update()

This function retrieves Reddit posts from the ReleaseTrain API and formats them into structured output.

Supported features:
- Subreddit selection (q)
- Minimum score filtering (minScore)
- Minimum comment filtering (minComments)
- Pagination (page)
- Field selection (fields)
- Sorting (ascending)
- Result limit (limit)

---

## CLI Interface

The CLI allows interaction with all system functionality.

Example:

python cli.py package-update --q programming,technology --limit 10

---

### Available Commands

| Command         | Description |
|----------------|-------------|
| package-update | Fetch Reddit posts |
| get-request    | Send HTTP GET request |
| capstone       | Print greeting message |
| agent-update   | Start AI agent conversation |
| help           | Show CLI help |
| -v / --version | Show CLI version |
| exit           | Exit CLI |

---

## package-update Command

Fetches and formats Reddit posts from the API.

Example:

python cli.py package-update --q python --limit 5

### Parameters

--q             Subreddits to query (default: programming, Python)  
--min-score     Minimum post score (default: 50)  
--min-comments  Minimum comment count (default: 10)  
--limit         Number of posts returned (default: 25)  
--page          Pagination page (default: 2)  
--fields        Fields returned from API  
--ascending     Sort order (0 or 1)

---

## AI Agent System (AgentUpdate)

The system includes an AI agent powered by Ollama (Llama 3.2) that can:

- Interpret user requests
- Decide when to call tools
- Execute approved Python functions
- Summarize results

---

## Agent Modes

### TOOL CALLING MODE

When no tool output is present, the model MUST respond with:

CALL_FUNCTION:
Update.package_update(...)

Rules:
- Always call a function
- Never answer directly
- Use defaults if needed
- Extract parameters from user input when possible

---

### SUMMARIZATION MODE

When tool output is present, the model must:

- Summarize Reddit results
- Highlight key posts and trends
- Provide useful links
- NOT call any functions

---

## TOOL REGISTRY

Only approved functions can be executed:

TOOL_REGISTRY = {
    "package_update": Update.package_update
}

This ensures:
- No unsafe function execution
- Controlled tool access
- Secure agent behavior

---

## Agent Workflow

1. User inputs request
2. LLM processes request
3. LLM optionally requests tool call
4. Python executes tool via TOOL_REGISTRY
5. Tool output is appended to conversation
6. LLM summarizes results
7. Loop continues until exit

---

## Example Agent Usage

from agenticRT import SYSTEM_PROMPT, TOOL_REGISTRY, AgentUpdate

AgentUpdate.agent_update_conversation(SYSTEM_PROMPT, TOOL_REGISTRY)

---

## API Layer

### Update.package_update()

Endpoint:

https://releasetrain.io/api/reddit/by-subreddit

Returns:
- URL
- Score
- Tags
- Title
- Subreddit
- Author description (if available)

---

## Output Format

[URL:] ...
[SCORE:] ...
[TAG(s):] ...
[TITLE:] ...
[SUBREDDIT:] ...
[AUTHOR_DESCRIPTION:] ...

---

## Future Improvements

- Add multiple tool support
- Improve agent loop stability
- Improve summarization formatting
- Expand tool registry safely
- Add streaming LLM responses
- Improve CLI output formatting 

---

## Design Philosophy

This project follows a controlled agent architecture:

- LLM cannot execute arbitrary code
- Python enforces strict tool access
- All actions go through a registry layer
- System alternates between:
  - Tool execution
  - Summarization

---

## Summary

PackageUpdateSearch combines:

- CLI tooling
- API integration
- Agent-based reasoning
- Safe function execution layer

It demonstrates a structured approach to building agentic Python systems.