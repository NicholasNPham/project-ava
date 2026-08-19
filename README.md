# AV Duration Calculator (ava.exe)

## 1. What Problem It Solves

Checking the runtime of a folder full of video and audio files one at a time, manually, is slow and easy to get wrong. This tool scans a folder, reads the real duration of every video/audio file in it, and reports a total, in seconds, with zero manual clicking through file properties.

## 2. How It Works

Drop `ava.exe` into a folder with video/audio files and double click it. The tool scans every file in that folder, checks whether it's a supported audio/video type, and skips anything that isn't (a warning is shown for each skipped file rather than silently ignoring it). For every supported file, it reads the actual duration straight from the file's own metadata rather than trusting the file extension, so a mislabeled file still gets read correctly. Results, including any files that couldn't be read, are shown in a simple popup window along with the combined total runtime.

## 3. Tech Used

- **Python** — core logic, folder scanning, subprocess orchestration
- **ffprobe** (part of FFmpeg) — reads accurate media duration directly from file metadata, bundled inside the executable, no separate install required
- **tkinter** — built-in Python GUI library, used for the results popup
- **PyInstaller** — packages the script and ffprobe into a single standalone `.exe` that runs on any Windows machine, no Python installation required

## 4. Results

**Before:** opening each video/audio file individually (right click → Properties, or opening it in a media player) to check its length, one file at a time, then manually adding up the total.

**After:** one double click. Every file in the folder is read automatically and a single total is reported.

## 5. How to Run It

1. Place `ava.exe` in a folder along with the video/audio files you want checked.
2. Double click `ava.exe`.
3. A popup window will display each file's name and duration, any excluded/unreadable files with a warning, and the total combined duration.
4. Close the window when done, no further action needed.

**Supported file types:** `.mp4` `.mov` `.avi` `.wmv` `.3gp` `.vob` `.asf` `.mpeg` `.wav` `.mp3` `.m4a` `.wma` `.aac`