## Prerequisites
Before setting up the environment, ensure you have the following installed:

+ Python 3.10+

+ UV (High-performance Python package manager)

+ Node.js (For MCP inspector and some clients)

## Setup & Installation
# 1. Clone the Repository
```bash
git clone https://github.com/toqeer-yasir/MCP.git
cd MCP
```
# 2. Environment Setup & Dependencies
```bash
# Initialize the project with UV
uv init .
```
Install FastMCP framework

```bash
uv add fastmcp
# or alternatively
uv pip install fastmcp
```
# 3. Verify Installation
```bash
python -c "import fastmcp; print('FastMCP installed successfully!')"
```
🧪 Testing Your Server
Development Mode
```bash
# Primary method with UV
uv fastmcp dev server_name.py
Alternative Methods
```
```bash
# Direct FastMCP command
fastmcp dev server_name.py
```
**If both above don't work, use MCP inspector**
```bash
npx @modelcontextprotocol/inspector python file_name.py
```
🏗️ **Project Structure**
*This repository contains:*

🔧 MCP Servers
Local MCP Servers - Run directly on your machine

Remote MCP Servers - Cloud-hosted MCP services

💻 MCP Clients
Client implementations to connect with MCP servers

Example integrations and usage patterns
Set up a local server:

```bash
cd servers/local
uv fastmcp dev your_server.py
```
Connect with a client:
```bash
cd clients
python client_example.py
```
___
