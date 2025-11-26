import os
import glob
import shutil
import stat
from pathlib import Path
from datetime import datetime
from fastmcp import FastMCP

mcp = FastMCP("File System")

@mcp.tool()
def read_file(file_path: str) -> str:
    """Read and return the entire content of the file."""
    with open(file_path, 'r', encoding= 'utf-8') as f:
        return f.read()
    
@mcp.tool()
def write_file(file_path: str, content: str, mode: str= 'w') -> str:
    """Write content to a file. Mode 'w' (write) or 'a' (append)."""
    with open(file_path, mode, encoding= 'utf-8') as f:
        f.write()
    return f"Successfully wrote to {file_path}"


@mcp.tool()
def list_dir(dir_path: str= '.', show_hidden: bool= False) -> str:
    """List all items in a directory with details."""
    path= Path(dir_path)
    items= []
    for item in path.iterdir():
        if not show_hidden and item.name.startswith('.'):
            continue
        
        if item.is_dir():
            items.append(f"📁 {item.name}/")
        elif item.is_file():
            size = item.stat().st_size
            items.append(f"📄 {item.name} ({size} bytes)")
        else:
            items.append(f"🔗 {item.name}")
    return  f"📁 {dir_path}:\n" + "\n".join(sorted(items))


@mcp.tool()
def file_info(file_path: str) -> str:
    """Get detailed metadata about a file or directory."""
    path = Path(file_path)
    if not path.exists():
        return f"❌ Path does not exist: {file_path}"
    
    stat = path.stat()
    modified = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
    
    if path.is_dir():
        item_type = "Directory"
        size = "N/A"
    else:
        item_type = "File"
        size = f"{stat.st_size} bytes ({stat.st_size/1024:.1f} KB)"
    
    return f"""
📊 File Information:
📍 Path: {file_path}
📝 Type: {item_type}
📏 Size: {size}
🕒 Modified: {modified}
🔒 Permissions: {oct(stat.st_mode)[-3:]}
👤 Owner: {stat.st_uid}
""".strip()

@mcp.tool()
def search_files(pattern: str, search_dir: str= '.', recursive: bool= True) -> str:
    """Search for files using wildcard patterns (*.py, *.txt, etc.)."""
    matches = list(Path(search_dir).rglob(pattern) if recursive else Path(search_dir).glob(pattern))
    if not matches:
        return f"No file found matching: {pattern}"
    
    result = [f"Found {len(matches)} files matching '{pattern}':"]
    for match in sorted(matches):
        result.append(f" 📄 {match}")
    
    return "\n".join(result)


@mcp.tool()
def create_directory(dir_path: str, parents: bool = True) -> str:
    """Create a new directory. Creates parent directories if needed."""
    Path(dir_path).mkdir(parents=parents, exist_ok=True)
    return f"✅ Created directory: {dir_path}"

@mcp.tool()
def delete_path(path: str) -> str:
    """Delete a file or directory (be careful!)."""
    path_obj = Path(path)
    
    if not path_obj.exists():
        return f"❌ Path does not exist: {path}"
    
    if path_obj.is_dir():
        shutil.rmtree(path)
        return f"✅ Deleted directory: {path}"
    else:
        path_obj.unlink()
        return f"✅ Deleted file: {path}"

@mcp.tool()
def get_current_directory() -> str:
    """Get the current working directory."""
    return f"📁 Current directory: {Path.cwd()}"


@mcp.tool()
def copy_file(source: str, destination: str) -> str:
    """Copy a file or directory to a new location."""
    source_path = Path(source)
    dest_path = Path(destination)
    
    if source_path.is_dir():
        shutil.copytree(source, destination)
        return f"✅ Copied directory: {source} → {destination}"
    else:
        shutil.copy2(source, destination)
        return f"✅ Copied file: {source} → {destination}"

@mcp.tool()
def move_file(source: str, destination: str) -> str:
    """Move or rename a file or directory."""
    shutil.move(source, destination)
    return f"✅ Moved: {source} → {destination}"

@mcp.tool()
def file_stats(directory: str = ".") -> str:
    """Get statistics about files in a directory."""
    path = Path(directory)
    files = list(path.rglob('*')) if path.is_dir() else []
    
    if not files:
        return "No files found."
    
    file_count = len([f for f in files if f.is_file()])
    dir_count = len([f for f in files if f.is_dir()])
    total_size = sum(f.stat().st_size for f in files if f.is_file())
    
    return f"""
📊 Directory Statistics:
📁 Location: {directory}
📄 Files: {file_count}
📂 Directories: {dir_count}
💾 Total Size: {total_size} bytes ({total_size/1024/1024:.1f} MB)
""".strip()


@mcp.tool()
def find_large_files(directory: str = ".", min_size_mb: int = 10) -> str:
    """Find files larger than specified size in MB."""
    large_files = []
    min_size = min_size_mb * 1024 * 1024
    
    for file_path in Path(directory).rglob('*'):
        if file_path.is_file():
            size = file_path.stat().st_size
            if size > min_size:
                large_files.append((file_path, size))
    
    if not large_files:
        return f"✅ No files larger than {min_size_mb} MB found."
    
    large_files.sort(key=lambda x: x[1], reverse=True)
    result = [f"📏 Files larger than {min_size_mb} MB:"]
    
    for file_path, size in large_files[:10]:  # Top 10 largest
        size_mb = size / (1024 * 1024)
        result.append(f"  📄 {file_path} ({size_mb:.1f} MB)")
    
    return "\n".join(result)


if __name__ == "__main__":
    mcp.run()