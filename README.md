# OpenAI agents

This repository contains a minimal re-implementation of [OpenAI's real-time agents repository](https://github.com/openai/openai-realtime-agents/tree/main) in Python.

## Installation

We recommend using [uv](https://docs.astral.sh/uv/) to install the dependencies.

```bash
pip install uv
uv venv
source .venv/bin/activate
uv add agents-poc
```

Next to that, you need to create a `keys.env` file in the root of the repository with the following variables:

```bash
OPENAI_API_KEY=<your-openai-api-key>
```

## Usage

```bash
uv run --env-file keys.env main.py
```

## Gradio demo

We also provide a Gradio interface to interact with the multi-agent system.

```bash
uv run --env-file keys.env app.py
```

### Who do I talk to? ###

* Repo owner: Niels Rogge
