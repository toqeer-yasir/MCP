from fastmcp import FastMCP
import subprocess
import os
import glob

mcp = FastMCP("Audio Control Server")

def get_music_directory():
    """Get the default music directory."""
    music_dirs = [
        os.path.expanduser("~/Music"),
        os.path.expanduser("~/music"), 
        os.path.expanduser("~/.local/share/rhythmbox"),
    ]
    for dir_path in music_dirs:
        if os.path.exists(dir_path):
            return dir_path
    return os.path.expanduser("~")

@mcp.tool()
def play_audio(file_path: str) -> str:
    """Play an audio file in VLC player."""
    if not os.path.exists(file_path):
        return "❌ Sorry, I couldn't find that file. Please check the path and try again."
    
    try:
        subprocess.Popen(["vlc", file_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        filename = os.path.basename(file_path)
        return f"🎵 Now playing: {filename}"
    except Exception as e:
        return f"❌ Oops! Couldn't start VLC. Make sure it's installed. Error: {str(e)}"

@mcp.tool()
def play_pause() -> str:
    """Play or pause the current track in VLC."""
    result = subprocess.run(["playerctl", "-p", "vlc", "play-pause"], capture_output=True, text=True)
    if result.returncode == 0:
        return "⏯️ Playback toggled"
    else:
        return "❌ VLC doesn't seem to be running. Try playing a song first!"

@mcp.tool()
def stop_audio() -> str:
    """Stop the audio playback completely."""
    result = subprocess.run(["playerctl", "-p", "vlc", "stop"], capture_output=True, text=True)
    if result.returncode == 0:
        return "⏹️ Music stopped"
    else:
        return "❌ No music is currently playing"

@mcp.tool()
def set_volume(level: int = 50) -> str:
    """Set the volume to a specific level (0-100)."""
    if level < 0 or level > 100:
        return "❌ Please choose a volume between 0 and 100"
    
    result = subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"{level}%"], capture_output=True)
    if result.returncode == 0:
        volume_emoji = "🔇" if level == 0 else "🔈" if level < 30 else "🔉" if level < 70 else "🔊"
        return f"{volume_emoji} Volume set to {level}%"
    else:
        return "❌ Couldn't adjust the volume. Is your audio system working?"

@mcp.tool()
def set_volume_up(increment: int = 10) -> str:
    """Turn the volume up by the specified amount."""
    result = subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"+{increment}%"], capture_output=True)
    if result.returncode == 0:
        return f"🔊 Volume increased by {increment}%"
    else:
        return "❌ Couldn't increase volume"

@mcp.tool()
def set_volume_down(decrement: int = 10) -> str:
    """Turn the volume down by the specified amount."""
    result = subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"-{decrement}%"], capture_output=True)
    if result.returncode == 0:
        return f"🔉 Volume decreased by {decrement}%"
    else:
        return "❌ Couldn't decrease volume"

@mcp.tool()
def next_track() -> str:
    """Skip to the next track in the playlist."""
    result = subprocess.run(["playerctl", "-p", "vlc", "next"], capture_output=True, text=True)
    if result.returncode == 0:
        return "⏭️ Skipping to next track..."
    else:
        return "❌ Can't skip track. Make sure VLC is playing and has a playlist!"

@mcp.tool()
def previous_track() -> str:
    """Go back to the previous track in the playlist."""
    result = subprocess.run(["playerctl", "-p", "vlc", "previous"], capture_output=True, text=True)
    if result.returncode == 0:
        return "⏮️ Going back to previous track..."
    else:
        return "❌ Can't go back. Make sure VLC is playing and has a playlist!"

@mcp.tool()
def seek_forward(seconds: int = 15) -> str:
    """Jump forward in the current track by specified seconds."""
    if seconds <= 0:
        return "❌ Please specify a positive number of seconds to jump forward"
    
    result = subprocess.run(["playerctl", "-p", "vlc", "position", f"{seconds}+"], capture_output=True, text=True)
    if result.returncode == 0:
        return f"⏩ Jumped forward {seconds} seconds"
    else:
        return "❌ Couldn't seek forward. Make sure VLC is playing a track!"

@mcp.tool()
def seek_backward(seconds: int = 15) -> str:
    """Jump backward in the current track by specified seconds."""
    if seconds <= 0:
        return "❌ Please specify a positive number of seconds to jump backward"
    
    result = subprocess.run(["playerctl", "-p", "vlc", "position", f"{seconds}-"], capture_output=True, text=True)
    if result.returncode == 0:
        return f"⏪ Jumped backward {seconds} seconds"
    else:
        return "❌ Couldn't seek backward. Make sure VLC is playing a track!"

@mcp.tool()
def seek_to_position(seconds: int = 0) -> str:
    """Jump to a specific position in the track (in seconds)."""
    if seconds < 0:
        return "❌ Please specify a positive time position"
    
    result = subprocess.run(["playerctl", "-p", "vlc", "position", str(seconds)], capture_output=True, text=True)
    if result.returncode == 0:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"⏱️ Jumped to {minutes}:{remaining_seconds:02d}"
    else:
        return "❌ Couldn't seek to position. Make sure VLC is playing a track!"

@mcp.tool()
def search_music(search_term: str, search_dir: str = None) -> str:
    """Search for music files by name in your music directory."""
    if search_dir is None:
        search_dir = get_music_directory()
    
    if not os.path.exists(search_dir):
        return f"❌ The directory {search_dir} doesn't exist. Please check the path."
    
    # Supported audio formats
    audio_extensions = ['*.mp3', '*.wav', '*.flac', '*.m4a', '*.aac', '*.ogg', '*.wma']
    
    found_files = []
    for extension in audio_extensions:
        pattern = os.path.join(search_dir, "**", extension)
        matches = glob.glob(pattern, recursive=True)
        for match in matches:
            filename = os.path.basename(match)
            if search_term.lower() in filename.lower():
                found_files.append(match)
    
    if not found_files:
        return f"🔍 No music files found matching '{search_term}' in {search_dir}"
    
    # Show top 10 results
    result = f"🎵 Found {len(found_files)} music files matching '{search_term}':\n\n"
    for i, file_path in enumerate(found_files[:10], 1):
        filename = os.path.basename(file_path)
        folder = os.path.basename(os.path.dirname(file_path))
        result += f"{i}. {filename}\n   📁 {folder}\n   📍 {file_path}\n\n"
    
    if len(found_files) > 10:
        result += f"... and {len(found_files) - 10} more files\n\n"
    
    result += "💡 Use 'play_audio' with the full path to play any of these songs!"
    return result

@mcp.tool()
def now_playing() -> str:
    """Get information about the currently playing track."""
    # Get basic metadata
    result = subprocess.run(["playerctl", "-p", "vlc", "metadata"], capture_output=True, text=True)
    
    if result.returncode != 0:
        return "❌ No music is currently playing. Try playing a song first!"
    
    # Parse the metadata
    lines = result.stdout.strip().split('\n')
    metadata = {}
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            metadata[key.strip()] = value.strip()
    
    # Build a friendly response
    title = metadata.get('xesam:title', 'Unknown Title')
    artist = metadata.get('xesam:artist', 'Unknown Artist')
    album = metadata.get('xesam:album', 'Unknown Album')
    
    response = "🎵 Now Playing:\n\n"
    response += f"📀 **Title:** {title}\n"
    response += f"👤 **Artist:** {artist}\n"
    response += f"💿 **Album:** {album}\n"
    
    # Get playback status and position
    status_result = subprocess.run(["playerctl", "-p", "vlc", "status"], capture_output=True, text=True)
    if status_result.returncode == 0:
        status = status_result.stdout.strip()
        status_emoji = "▶️" if status == "Playing" else "⏸️" if status == "Paused" else "⏹️"
        response += f"📊 **Status:** {status_emoji} {status}\n"
    
    # Try to get current position
    position_result = subprocess.run(["playerctl", "-p", "vlc", "position"], capture_output=True, text=True)
    if position_result.returncode == 0 and position_result.stdout.strip():
        try:
            position_seconds = float(position_result.stdout.strip())
            minutes = int(position_seconds // 60)
            seconds = int(position_seconds % 60)
            response += f"⏱️ **Position:** {minutes}:{seconds:02d}\n"
        except:
            pass
    
    return response


if __name__ == "__main__":
    mcp.run()