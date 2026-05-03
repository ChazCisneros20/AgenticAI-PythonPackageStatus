"""
Interactive Ollama agent that summarizes Reddit updates using `Update.package_update`.

Prerequisites:
    pip install PackageUpdateSearch
    Ollama running locally (default http://localhost:11434)
    Model pulled, e.g.: ollama pull llama3.2:3b

Run:
    python examples/example_agent_update.py

Type your question at the prompt; type 'exit' to quit.
"""

from PackageUpdateSearch.agenticRT import AgentUpdate


def main() -> None:
    AgentUpdate.agent_update_conversation()


if __name__ == "__main__":
    main()
