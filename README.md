# MCP Server

A Model Context Protocol (MCP) server built using the FastMCP framework. This server provides tools and resources for various tasks and integrations.

## Prerequisites

Before setting up the environment, make sure you have the following installed:

- **Python 3.10+**
- **uv** (package manager faster than *pip* and compatible with fastmcp)

- ## Setup

### 1. Clone the Repository
```bash
git clone https://github.com/toqeer-yasir/MCP.git
cd MCP
```
### 2. Installation & Inintialization
1) uv init .
2) uv add fastmcp or uv pip install fastmcp

## How to test server?
```bash
uv fastmcp dev servr_name.py
```
*or*
```bash
fastmcp dev server_name.py
```
*If both above dosen't work then try this:*
```bash
npx @modelcontextprotocol/inspector python file_name.py
```
-
