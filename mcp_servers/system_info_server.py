import psutil
import platform
from fastmcp import FastMCP

mcp = FastMCP("System Info Server")

@mcp.tool()
def system_status() -> str:
    """Get basic system overview (CPU, memory, disk, OS)."""
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    return f"""
System Status:
CPU: {cpu}% | Memory: {memory.percent}% | Disk: {disk.percent}%
OS: {platform.system()} {platform.release()}
""".strip()

@mcp.tool()
def memory_info() -> str:
    """Get detailed memory usage."""
    mem = psutil.virtual_memory()
    return f"Memory: {mem.percent}% used ({mem.used//1024//1024}MB / {mem.total//1024//1024}MB)"

@mcp.tool()
def disk_info() -> str:
    """Get disk usage for root partition."""
    disk = psutil.disk_usage('/')
    return f"Disk: {disk.percent}% used ({disk.used//1024//1024//1024}GB / {disk.total//1024//1024//1024}GB)"

@mcp.tool()
def top_processes(n: int = 5) -> str:
    """Get top N processes by CPU usage."""
    procs = []
    for p in psutil.process_iter(['name', 'cpu_percent']):
        try:
            procs.append(p.info)
        except:
            pass
    
    procs.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
    result = "Top processes:\n"
    for i, p in enumerate(procs[:n], 1):
        result += f"{i}. {p['name']}: {p['cpu_percent'] or 0:.1f}%\n"
    return result.strip()

if __name__ == "__main__":
    mcp.run()