import copy
from types import SimpleNamespace

import pytest

from PackageUpdateSearch import agenticRT


class _FakeToolCall:
    def __init__(self, name, arguments):
        self.function = SimpleNamespace(name=name, arguments=arguments)


class _FakeMessage:
    def __init__(self, content="", tool_calls=None):
        self.content = content
        self.tool_calls = tool_calls or []


class _FakeResponse:
    def __init__(self, message):
        self.message = message


class _FakeClient:
    def __init__(self, scripted_messages):
        self._scripted_messages = list(scripted_messages)
        self.calls = []

    def chat(self, **kwargs):
        self.calls.append(copy.deepcopy(kwargs))
        if not self._scripted_messages:
            raise AssertionError("No scripted model messages left")
        return _FakeResponse(self._scripted_messages.pop(0))


def test_agent_loop_runs_tool_then_summary_for_minimum_score_phrase(monkeypatch, capsys):
    """Ensure loop executes model-provided minScore from noisy user wording."""
    recorded = []

    def fake_package_update(**kwargs):
        recorded.append(kwargs)
        return (
            "[URL: ] https://reddit.com/r/typescript/comments/abc\n"
            "[SCORE: ] 15\n"
            "[TAG(s): ] []\n"
            "[TITLE: ] TypeScript update\n"
            "[SUBREEDDIT: ] typescript\n"
            "[AUTHOR_DESCRIPTION: ]\n\n"
        )

    fake_client = _FakeClient(
        [
            _FakeMessage(
                tool_calls=[
                    _FakeToolCall(
                        "package_update",
                        {
                            "q": "TypeScript",
                            "minScore": 15,
                            "minComments": 10,
                            "limit": 5,
                            "page": 1,
                            "fields": "url,score,tag,title,subreddit,author_description",
                            "ascending": 1,
                        },
                    )
                ]
            ),
            _FakeMessage(
                content=(
                    "============SUMMARY============\n"
                    "TypeScript discussions emphasize practical updates.\n\n"
                    "- TypeScript update (score: 15)\n"
                    "============SUMMARY============\n"
                    "### Key Reddit links (verbatim)\n"
                    "- https://reddit.com/r/typescript/comments/abc\n"
                    "### Grounding rule\n"
                    "Every URL above is copied from a [URL: ] line in the latest tool message."
                )
            ),
        ]
    )

    inputs = iter(
        [
            "Any updates with a minimum score for of 15 on TypeScript?",
            "exit",
        ]
    )

    monkeypatch.setattr(agenticRT.AgentUpdate, "is_ollama_running", staticmethod(lambda: True))
    monkeypatch.setattr(agenticRT, "Client", lambda: fake_client)
    monkeypatch.setattr("builtins.input", lambda _prompt="": next(inputs))

    agenticRT.AgentUpdate.agent_update_conversation(
        SYSTEM_PROMPT=agenticRT.SYSTEM_PROMPT,
        TOOL_REGISTRY={"package_update": fake_package_update},
    )

    output = capsys.readouterr().out

    assert recorded, "Expected package_update to be called at least once"
    assert recorded[0]["minScore"] == 15
    assert "============SUMMARY============" in output
    assert "TypeScript update (score: 15)" in output


def test_agent_loop_keeps_user_query_text_for_model_interpretation(monkeypatch):
    """The raw user phrase should reach model messages unchanged."""
    fake_client = _FakeClient(
        [
            _FakeMessage(
                tool_calls=[
                    _FakeToolCall(
                        "package_update",
                        {
                            "q": "TypeScript",
                            "minScore": 15,
                            "minComments": 10,
                            "limit": 5,
                            "page": 1,
                            "fields": "url,score,tag,title,subreddit,author_description",
                            "ascending": 1,
                        },
                    )
                ]
            ),
            _FakeMessage(content="done"),
        ]
    )

    inputs = iter(["with a minimum score for of 15", "exit"])

    monkeypatch.setattr(agenticRT.AgentUpdate, "is_ollama_running", staticmethod(lambda: True))
    monkeypatch.setattr(agenticRT, "Client", lambda: fake_client)
    monkeypatch.setattr(
        "builtins.input",
        lambda _prompt="": next(inputs),
    )

    agenticRT.AgentUpdate.agent_update_conversation(
        SYSTEM_PROMPT=agenticRT.SYSTEM_PROMPT,
        TOOL_REGISTRY={"package_update": lambda **_kwargs: ""},
    )

    first_chat_messages = fake_client.calls[0]["messages"]
    assert first_chat_messages[1]["role"] == "user"
    assert first_chat_messages[1]["content"] == "with a minimum score for of 15"


@pytest.mark.parametrize(
    "user_prompt",
    [
        "with a minimum score of 15",
        "with a minimum score for of 15",
        "minimum score 15 for typescript",
        "show posts min score 15",
        "score >= 15 on TypeScript",
    ],
)
def test_agent_loop_handles_min_score_phrase_variants(monkeypatch, user_prompt):
    recorded = []

    def fake_package_update(**kwargs):
        recorded.append(kwargs)
        return ""

    fake_client = _FakeClient(
        [
            _FakeMessage(
                tool_calls=[
                    _FakeToolCall(
                        "package_update",
                        {
                            "q": "TypeScript",
                            "minScore": 15,
                            "minComments": 10,
                            "limit": 3,
                            "page": 1,
                            "fields": "url,score,tag,title,subreddit,author_description",
                            "ascending": 1,
                        },
                    )
                ]
            ),
            _FakeMessage(content="summary"),
        ]
    )

    inputs = iter([user_prompt, "exit"])
    monkeypatch.setattr(agenticRT.AgentUpdate, "is_ollama_running", staticmethod(lambda: True))
    monkeypatch.setattr(agenticRT, "Client", lambda: fake_client)
    monkeypatch.setattr("builtins.input", lambda _prompt="": next(inputs))

    agenticRT.AgentUpdate.agent_update_conversation(
        SYSTEM_PROMPT=agenticRT.SYSTEM_PROMPT,
        TOOL_REGISTRY={"package_update": fake_package_update},
    )

    assert recorded
    assert recorded[0]["minScore"] == 15


def test_agent_loop_resets_messages_between_queries_by_default(monkeypatch):
    fake_client = _FakeClient(
        [
            _FakeMessage(
                tool_calls=[
                    _FakeToolCall(
                        "package_update",
                        {
                            "q": "TypeScript",
                            "minScore": 15,
                            "minComments": 10,
                            "limit": 2,
                            "page": 1,
                            "fields": "url,score,tag,title,subreddit,author_description",
                            "ascending": 1,
                        },
                    )
                ]
            ),
            _FakeMessage(content="summary one"),
            _FakeMessage(
                tool_calls=[
                    _FakeToolCall(
                        "package_update",
                        {
                            "q": "Python",
                            "minScore": 25,
                            "minComments": 10,
                            "limit": 2,
                            "page": 1,
                            "fields": "url,score,tag,title,subreddit,author_description",
                            "ascending": 1,
                        },
                    )
                ]
            ),
            _FakeMessage(content="summary two"),
        ]
    )

    inputs = iter(["minimum score 15 typescript", "python min score 25", "exit"])
    monkeypatch.setattr(agenticRT.AgentUpdate, "is_ollama_running", staticmethod(lambda: True))
    monkeypatch.setattr(agenticRT, "Client", lambda: fake_client)
    monkeypatch.setattr("builtins.input", lambda _prompt="": next(inputs))

    agenticRT.AgentUpdate.agent_update_conversation(
        SYSTEM_PROMPT=agenticRT.SYSTEM_PROMPT,
        TOOL_REGISTRY={"package_update": lambda **_kwargs: ""},
    )

    # call order: tool call #1, summary #1, tool call #2, summary #2
    second_cycle_tool_call_messages = fake_client.calls[2]["messages"]
    assert len(second_cycle_tool_call_messages) == 2
    assert second_cycle_tool_call_messages[0]["role"] == "system"
    assert second_cycle_tool_call_messages[1]["role"] == "user"
    assert second_cycle_tool_call_messages[1]["content"] == "python min score 25"
