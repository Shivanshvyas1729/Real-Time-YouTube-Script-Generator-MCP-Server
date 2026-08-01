# 🎬 Real-Time YouTube Script Generator & MCP Server

![project structure](assests/3242.png)




An AI-powered application that retrieves real-time web information using **Tavily Search** and converts it into high-retention, production-ready short video scripts (YouTube Shorts / Instagram Reels) using **Gemini LLM**.

The project features both a **Streamlit Web App** interface and a **FastMCP (Model Context Protocol) Server** for seamless integration with AI assistants (Claude, Cursor, etc.).

---

## ✨ Features

- 🔍 **Real-Time Web Search**: Integrates Tavily API for fetching up-to-date web data.
- 📌 **AI Summarization**: Automatically synthesizes search snippets into concise, structured summaries.
- 📜 **Production-Ready Script Generation**: Formats context into short-video scripts complete with visual cues, verbal hooks, and call-to-actions.
- 💻 **Interactive Streamlit Web UI**: Simple web browser interface to search, preview, and download scripts as `.txt`.
- 🔌 **Model Context Protocol (FastMCP)**: Exposes search and script generation tools as standard MCP endpoints for external AI clients.

---

## 🛠️ Project Structure

```text
├── app.py              # Streamlit web application & core logic (Tavily + LLM)
├── mcp_server.py       # FastMCP server exposing tool endpoints
├── assests/            # Project diagrams & images
│   └── 3242.png
├── pyproject.toml      # Project configuration & dependencies
├── .env                # API keys configuration (not committed)
└── README.md           # Project documentation
```

---

## 🔑 Environment Setup

Create a `.env` file in the root directory:

```env
AICREDITS_API_KEY=your_aicredits_or_openai_key
TAVILY_API_KEY=your_tavily_api_key
```

---

## 📦 Installation

Using [`uv`](https://github.com/astral-sh/uv) (recommended):

```cmd
uv sync
```

---

## 🚀 Usage

### 1. Run the Streamlit Web Application

To launch the interactive web interface:

```cmd
uv run streamlit run app.py
```

Open your browser at `http://localhost:8501`.

### 2. Test/Dev MCP Server with FastMCP Inspector

To test the MCP tools (`get_latest_info_mcp` and `get_video_script_mcp`) in an interactive browser UI:

```cmd
uv run mcp dev mcp_server.py
```

### 3. Connect MCP Server to Claude / Cursor

Add the server definition to your MCP client configuration (e.g. `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "youtube-script-generator": {
      "command": "uv",
      "args": ["run", "python", "C:/Users/DELL/Desktop/New folder/mcp_server.py"]
    }
  }
}
```

---

## 🛠️ MCP Tools Offered

| Tool Name | Description |
|---|---|
| `get_latest_info_mcp(query)` | Performs a real-time web search and returns an AI summary. |
| `get_video_script_mcp(query)` | Fetches real-time web search data and generates a production-ready script. |


![user workflow](assests/1.png)