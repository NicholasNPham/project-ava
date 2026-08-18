import subprocess
from key import executable_path, video_path

command = [executable_path, "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", video_path]

try:
    subprocess.run(command, check=True)
    print("Process Finished Successfully!")
except FileNotFoundError:
    print(f"Error: The executable at '{executable_path}' was not found.")
except subprocess.CalledProcessError as e:
    print(f"The executable crashed with exit code {e.returncode}")