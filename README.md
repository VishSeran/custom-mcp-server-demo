# custom-mcp-server-demo

A beginner-friendly, notebook-based walkthrough of building MCP servers and clients from scratch with **FastMCP** — covering in-memory, STDIO, and HTTP transports, and wiring it all up to a LangChain/LangGraph ReAct agent.


## Overview

This project is a single Jupyter notebook (`FINAL_Hello_World_of_MCP_Servers.ipynb`) that introduces the **Model Context Protocol (MCP)** from the ground up using the [FastMCP](https://gofastmcp.com/getting-started/welcome) framework, which wraps the official MCP SDK.

It starts with plain LangChain tools for context, then builds a small **CalculatorMCPServer**, exposes it over three different transports, and finishes by connecting everything to a LangGraph ReAct agent that can call tools across multiple MCP servers at once.

## Objectives

By working through this notebook you will be able to:

- Use FastMCP to create MCP servers over both **STDIO** and **HTTP** transports
- Register custom **tools**, **resources**, and **prompts** on an MCP server
- Test MCP servers with client connections and manual tool calls
- Build a **multi-server client** and a **ReAct agent** that uses tools from all connected servers

## What's Inside

### 1. Setup
- Installs `fastmcp`, `langchain`, `langchain-mcp-adapters`, `langgraph`, and `langchain_openai`
- Helper functions for:
  - Creating a local `path/` directory used by file-based resources
  - Checking whether a port is free before starting an HTTP server (important in shared Jupyter environments)
  - Inspecting read/write streams and session IDs

### 2. LangChain Tools (baseline)
- A quick look at the `@tool` decorator to show how plain Python functions become LangChain-compatible tools, for comparison against MCP tools later.

### 3. Building `CalculatorMCPServer`
- Creates a `FastMCP` server instance with a name and instructions
- **Tools**: `add`, `subtract` (registered via `@mcp.tool`)
- **Resources**: two file-reading resource patterns
  - `file:///endpoint/{name}` — returns a templated string (no real file I/O)
  - `file://endpoint2/{name}` — reads real files from a local `path/` directory, including error handling for missing files
- **Prompts**: `review_code` — a reusable prompt template registered via `@mcp.prompt`

### 4. In-Memory Client
- Connects a `Client` directly to the in-process `mcp` server object (no transport needed)
- Calls tools (`add`), reads resources, and fetches prompts
- Explores response objects: `.data`, `.content[0].text`, `.structured_content`
- Inspects tool metadata: `list_tools()`, `inputSchema`, `outputSchema`
- Includes a hands-on exercise: write and call a `subtract` tool

### 5. HTTP Transport
- Starts the MCP server as a background HTTP service (`mcp.run_http_async(port=PORT)`) with a `/mcp` JSON-RPC endpoint
- Connects via `StreamableHttpTransport`
- Converts MCP tools to LangChain tools using `langchain_mcp_adapters.tools.load_mcp_tools`
- Builds a LangGraph `create_react_agent` that uses the live MCP session's tools
- Includes an exercise: write a function to list all tools from the HTTP client

### 6. STDIO Transport
- Writes a standalone `stdio_server.py` script (since STDIO servers can't run as an in-process function in Jupyter)
- Connects via `StdioTransport`, which spawns the server as a child process and communicates over `stdin`/`stdout`
- Mirrors the HTTP examples: manual tool calls, LangChain tool conversion, and a ReAct agent
- Includes an exercise: implement a `test_client` function for the STDIO client
- Notes on how this maps to `mcp.json`-style configuration used by tools like Cursor or Claude Desktop

### 7. Multiple MCP Servers
- Uses `MultiServerMCPClient` to connect to **both** the STDIO and HTTP servers simultaneously
- Loads and lists tools from both servers in one call (`client.get_tools()`)
- Builds a single ReAct agent with `gpt-5-nano` that can use tools from either server
- Walks through the resulting conversation trace (`HumanMessage` → `AIMessage` tool call → `ToolMessage` → final `AIMessage`)

## Requirements

- Python 3.10+
- Jupyter Notebook / JupyterLab
- An OpenAI API key (used by `langchain_openai` / the `gpt-5-nano` model in the agent examples)
- Packages (pinned versions used in the notebook):
  ```
  fastmcp==2.12.2
  langchain==0.3.27
  langchain_mcp_adapters==0.1.9
  langgraph==0.6.7
  langchain_openai==0.3.33
  ```

## Setup

```bash
# Clone the repo
git clone <this-repo-url>
cd custom-mcp-server-demo

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate

# Install dependencies
pip install fastmcp==2.12.2 langchain==0.3.27 langchain_mcp_adapters==0.1.9 langgraph==0.6.7 langchain_openai==0.3.33
```

Set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY=your_api_key_here
```

## Usage

Launch Jupyter and open the notebook:

```bash
jupyter notebook FINAL_Hello_World_of_MCP_Servers.ipynb
```

Run the cells top to bottom. A few things to keep in mind:

- **Port conflicts**: If you change or rerun the HTTP server, you must change the `PORT` variable first — reusing a port that's in use can crash the Jupyter kernel.
- **STDIO server file**: The notebook writes `stdio_server.py` to disk; keep it in the same directory as the notebook so relative paths resolve correctly.
- **Exercises**: Several cells are left blank with a "Click here for Solution" dropdown — try them yourself before revealing the answer.

## Project Structure

```
custom-mcp-server-demo/
├── FINAL_Hello_World_of_MCP_Servers.ipynb   # Main lab notebook
├── stdio_server.py                          # Generated during the notebook (STDIO transport server)
└── path/                                    # Generated during the notebook (sample files for resources)
    ├── examples.txt
    └── README.txt
```

## Key Concepts Covered

| Concept | Description |
|---|---|
| **Tools** | Active capabilities an agent can call to perform actions (`add`, `subtract`) |
| **Resources** | Passive, URI-addressed data an agent can read (templated strings or real files) |
| **Prompts** | Reusable, parameterized prompt templates (`review_code`) |
| **In-Memory Transport** | Client and server share a process — no network layer needed |
| **STDIO Transport** | Client spawns the server as a subprocess and talks over stdin/stdout |
| **HTTP Transport** | Server runs as a persistent web service reachable by URL |
| **MultiServerMCPClient** | Connects to several MCP servers at once and merges their tools for a single agent |

## Conclusion

This notebook demonstrates the fundamentals of MCP servers and their role in bridging LLMs with external tools and services — connecting via STDIO and HTTP transports, interacting with tools consistently regardless of transport, and applying async patterns for non-blocking communication.

