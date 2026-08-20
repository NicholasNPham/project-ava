# STANDARD LIBRARY IMPORTS
import subprocess
import sys
import os
import tkinter as tk
from pathlib import Path

# CONSTANTS
ALLOWED_EXTENSIONS = {".mp4", ".mov", ".avi", ".wmv", ".3gp", ".vob", ".asf", ".mpeg", ".wav", ".mp3", ".m4a", ".wma", ".aac"}

# HELPER FUNCTION
def path_to_ffprobe():
    if getattr(sys, 'frozen', False):
        ffprobe_dir = sys._MEIPASS
        scan_dir = os.path.dirname(sys.executable)
    else:
        ffprobe_dir = os.path.dirname(os.path.abspath(__file__))
        scan_dir = ffprobe_dir

    executable_path = os.path.join(ffprobe_dir, "ffprobe.exe")
    return executable_path, scan_dir

def time_format(seconds):
    hours = int( seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int((seconds % 3600) % 60)

    return f"{str(hours).zfill(2)}:{str(minutes).zfill(2)}:{str(seconds).zfill(2)}"

# FUNCTIONS
def build_command(video_path):

    executable_path, _ = path_to_ffprobe()

    return [executable_path, "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", video_path]

def get_files_in_folder(folder_path):

    files_list = []

    base_dir = Path(folder_path)

    for item in base_dir.iterdir():
        if item.is_file():
            files_list.append(item)

    return files_list

def run_ffprobe(video_path):
    result = subprocess.run(build_command(video_path), capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
    total_seconds = float(result.stdout.strip())
    result_line = f"{video_path.name}: {time_format(total_seconds)}"

    return total_seconds, result_line

# MAIN LOOP

result_lines = []

try:
    executable_path, base_dir = path_to_ffprobe()
    total_file_time_duration = 0
    all_files = get_files_in_folder(base_dir)


    target_folder_line = f"Target Folder: {base_dir}"
    result_lines.append(target_folder_line)

    for file in all_files:
        if file.suffix.lower() not in ALLOWED_EXTENSIONS:
            exclude_warning_line = f"WARNING: Excluded File: {file.name}"
            result_lines.append(exclude_warning_line)
        else:
            try:
                total_seconds, result_line = run_ffprobe(file)
                total_file_time_duration += total_seconds
                result_lines.append(result_line)
            except subprocess.CalledProcessError as e:
                process_error_line = f"Error: The executable crashed with exit code {e.returncode} for file {file.name}"
                result_lines.append(process_error_line)

    formatted_time = time_format(total_file_time_duration)

    success_line = "Process Finished Successfully!"
    result_lines.append(success_line)
    total_line = f"Total Time: {formatted_time}"
    result_lines.append(total_line)

except FileNotFoundError:
    executable_path, _ = path_to_ffprobe()
    file_not_found_error = f"Error: The executable at '{executable_path}' was not found."
    result_lines.append(file_not_found_error)
except subprocess.CalledProcessError as e:
    process_error = f"The executable crashed with exit code {e.returncode}"
    result_lines.append(process_error)
finally:
    root = tk.Tk()
    root.title("AUDIO/VIDEO Duration Calculator")
    root.geometry("700x300")

    listbox = tk.Listbox(root)
    for line in result_lines:
        listbox.insert(tk.END, line)

    listbox.pack(pady=20, fill=tk.BOTH, expand=True)

    root.mainloop()