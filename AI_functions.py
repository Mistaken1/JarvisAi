import os
import sys
import subprocess
import shutil
import threading
import time
import webbrowser
import pyautogui
import psutil
import winreg
import ctypes
from datetime import datetime
from winotify import Notification, audio
import random
from io import BytesIO
import base64
import json
import winshell
# ─────────────────────────────────────────────
# NOTE: Response strings have been removed.
# Gemini now generates all spoken replies naturally.
# Functions return plain factual strings or None.
# ─────────────────────────────────────────────


# ─────────────────────────────────────────────
# APP CONTROL
# ─────────────────────────────────────────────

def open_app(app_name: str) -> str:
    try:
        os.startfile(app_name)
        return f"opened:{app_name}"
    except Exception as e:
        return f"error:open_app:{e}"

def close_app(app_name: str) -> str:
    closed = []
    for proc in psutil.process_iter(['name']):
        if app_name.lower() in proc.info['name'].lower():
            proc.kill()
            closed.append(proc.info['name'])
    if closed:
        return f"closed:{', '.join(closed)}"
    return f"error:no_process_found:{app_name}"

def list_running_apps() -> str:
    apps = set()
    for proc in psutil.process_iter(['name']):
        try:
            apps.add(proc.info['name'])
        except:
            pass
    return ', '.join(sorted(apps))


# ─────────────────────────────────────────────
# SYSTEM
# ─────────────────────────────────────────────

def shutdown_computer() -> str:
    subprocess.call(["shutdown", "/s", "/t", "5"])
    return "shutdown_initiated:5s"

def restart_computer() -> str:
    subprocess.call(["shutdown", "/r", "/t", "5"])
    return "restart_initiated:5s"

def sleep_computer() -> str:
    subprocess.call(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"])
    return "sleep_initiated"

def lock_computer() -> str:
    ctypes.windll.user32.LockWorkStation()
    return "screen_locked"

def get_battery_status() -> str:
    battery = psutil.sensors_battery()
    if battery:
        status = "charging" if battery.power_plugged else "not charging"
        return f"{battery.percent}% battery, {status}"
    return "error:no_battery_found"

def get_cpu_usage() -> str:
    usage = psutil.cpu_percent(interval=1)
    return f"CPU usage: {usage}%"

def get_ram_usage() -> str:
    ram = psutil.virtual_memory()
    used = round(ram.used / 1e9, 1)
    total = round(ram.total / 1e9, 1)
    return f"RAM: {ram.percent}% used ({used}GB / {total}GB)"


# ─────────────────────────────────────────────
# SCREEN / INPUT
# ─────────────────────────────────────────────

def take_screenshot(filename: str = "") -> str:
    if not filename:
        filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    path = os.path.join(os.path.expanduser("~"), "Pictures", filename)
    pyautogui.screenshot(path)
    return f"screenshot_saved:{path}"

def type_text(text: str) -> str:
    time.sleep(1)
    pyautogui.typewrite(text, interval=0.05)
    return f"typed:{text}"

def press_key(key: str) -> str:
    pyautogui.press(key)
    return f"pressed:{key}"

def scroll_up() -> str:
    pyautogui.scroll(5)
    return "scrolled_up"

def scroll_down() -> str:
    pyautogui.scroll(-5)
    return "scrolled_down"

def zoom_in() -> str:
    pyautogui.hotkey('ctrl', '+')
    return "zoomed_in"

def zoom_out() -> str:
    pyautogui.hotkey('ctrl', '-')
    return "zoomed_out"

def analyze_screen(question: str) -> str:
    """Returns base64-encoded PNG of the screen. Handled specially in Ajin.py."""
    screenshot = pyautogui.screenshot()
    buffer = BytesIO()
    screenshot.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

def click_at(x: int, y: int) -> str:
    """Moves the mouse to (x, y) and clicks."""
    pyautogui.click(x, y)
    return f"clicked:({x},{y})"

def right_click_at(x: int, y: int) -> str:
    """Right-clicks at (x, y)."""
    pyautogui.rightClick(x, y)
    return f"right_clicked:({x},{y})"

def double_click_at(x: int, y: int) -> str:
    """Double-clicks at (x, y)."""
    pyautogui.doubleClick(x, y)
    return f"double_clicked:({x},{y})"

def move_mouse(x: int, y: int) -> str:
    """Moves mouse to (x, y) without clicking."""
    pyautogui.moveTo(x, y, duration=0.3)
    return f"mouse_moved:({x},{y})"

def drag_mouse(from_x: int, from_y: int, to_x: int, to_y: int) -> str:
    """Drags from one position to another."""
    pyautogui.drag(from_x, from_y, to_x - from_x, to_y - from_y, duration=0.5)
    return f"dragged:({from_x},{from_y})->({to_x},{to_y})"

def get_mouse_position() -> str:
    """Returns current mouse cursor position."""
    x, y = pyautogui.position()
    return f"mouse_position:({x},{y})"

def hotkey(keys: str) -> str:
    """
    Presses a keyboard shortcut. Pass keys as comma-separated string.
    E.g. 'ctrl,c' for copy, 'ctrl,alt,delete', 'alt,f4', etc.
    """
    key_list = [k.strip() for k in keys.split(',')]
    pyautogui.hotkey(*key_list)
    return f"hotkey:{'+'.join(key_list)}"

def get_screen_size() -> str:
    """Returns the screen resolution."""
    w, h = pyautogui.size()
    return f"screen_size:{w}x{h}"


# ─────────────────────────────────────────────
# VOLUME
# ─────────────────────────────────────────────

def volume_up() -> str:
    for _ in range(5):
        pyautogui.press('volumeup')
    return "volume_increased"

def volume_down() -> str:
    for _ in range(5):
        pyautogui.press('volumedown')
    return "volume_decreased"

def mute_volume() -> str:
    pyautogui.press('volumemute')
    return "volume_muted"


# ─────────────────────────────────────────────
# BROWSER / WEB
# ─────────────────────────────────────────────

def open_website(url: str) -> str:
    if not url.startswith("http"):
        url = "https://" + url
    webbrowser.open(url)
    return f"opened_website:{url}"

def search_web(query: str) -> str:
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)
    return f"searched_google:{query}"

def clear_chrome_history() -> str:
    path = os.path.expanduser(r"~\AppData\Local\Google\Chrome\User Data\Default\History")
    try:
        os.remove(path)
        return "chrome_history_cleared"
    except Exception as e:
        return f"error:clear_chrome:{e}"

def clear_edge_history() -> str:
    path = os.path.expanduser(r"~\AppData\Local\Microsoft\Edge\User Data\Default\History")
    try:
        os.remove(path)
        return "edge_history_cleared"
    except Exception as e:
        return f"error:clear_edge:{e}"


# ─────────────────────────────────────────────
# FILES & FOLDERS
# ─────────────────────────────────────────────

def empty_recycle_bin() -> str:
    try:
        winshell = __import__("winshell")
        winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)
        return "recycle_bin_emptied"
    except Exception as e:
        return f"error:recycle_bin:{e}"

def open_folder(path: str) -> str:
    try:
        os.startfile(path)
        return f"opened_folder:{path}"
    except Exception as e:
        return f"error:open_folder:{e}"

def create_folder(path: str) -> str:
    try:
        os.makedirs(path, exist_ok=True)
        return f"folder_created:{path}"
    except Exception as e:
        return f"error:create_folder:{e}"

def delete_file(path: str) -> str:
    try:
        os.remove(path)
        return f"file_deleted:{path}"
    except Exception as e:
        return f"error:delete_file:{e}"



# ─────────────────────────────────────────────
# MUSIC / MEDIA
# ─────────────────────────────────────────────

def play_pause_media() -> str:
    pyautogui.press('playpause')
    return "media_toggled"

def next_track() -> str:
    pyautogui.press('nexttrack')
    return "next_track"

def previous_track() -> str:
    pyautogui.press('prevtrack')
    return "previous_track"

def play_music_from_folder(folder: str = "") -> str:
    if not folder:
        folder = os.path.join(os.path.expanduser("~"), "Music")
    for f in os.listdir(folder):
        if f.endswith((".mp3", ".wav", ".flac")):
            os.startfile(os.path.join(folder, f))
            return f"playing:{f}"
    return "error:no_music_found"


# ─────────────────────────────────────────────
# TIMERS & REMINDERS
# ─────────────────────────────────────────────

def set_timer(seconds: int) -> str:
    def _timer():
        time.sleep(seconds)
        toast = Notification(
            app_id="Ajin",
            title="Timer Done!",
            msg=f"Your {seconds} second timer has finished.",
        )
        toast.set_audio(audio.Default, loop=False)
        toast.show()
    threading.Thread(target=_timer, daemon=True).start()
    return f"timer_set:{seconds}s"

def set_reminder(message: str, seconds: int) -> str:
    def _reminder():
        with open("reminders.json", "a") as f:
            json.dump({"message": message, "time": time.time() + seconds}, f)
            f.write("\n")
        time.sleep(seconds)
        toast = Notification(
            app_id="Ajin",
            title="Reminder",
            msg=message,
        )
        toast.set_audio(audio.Default, loop=False)
        toast.show()
    threading.Thread(target=_reminder, daemon=True).start()
    return f"reminder_set:'{message}':{seconds}s"


# ─────────────────────────────────────────────
# CLIPBOARD
# ─────────────────────────────────────────────

def get_clipboard() -> str:
    try:
        import pyperclip
        content = pyperclip.paste()
        return f"clipboard_contents:{content}"
    except Exception as e:
        return f"error:clipboard_read:{e}"

def set_clipboard(text: str) -> str:
    try:
        import pyperclip
        pyperclip.copy(text)
        return f"clipboard_set:{text}"
    except Exception as e:
        return f"error:clipboard_write:{e}"


# ─────────────────────────────────────────────
# MISC
# ─────────────────────────────────────────────

def get_current_time() -> str:
    return datetime.now().strftime("%I:%M %p, %A %B %d %Y")

def run_command(command: str) -> str:
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
        output = result.stdout or result.stderr
        return output if output else "command_ran:no_output"
    except Exception as e:
        return f"error:run_command:{e}"

def get_commands() -> str:
    return """
APP CONTROL: open_app, close_app, list_running_apps
SYSTEM: shutdown_computer, restart_computer, sleep_computer, lock_computer, get_battery_status, get_cpu_usage, get_ram_usage
SCREEN/INPUT: take_screenshot, analyze_screen, type_text, press_key, hotkey, scroll_up, scroll_down, zoom_in, zoom_out
MOUSE: click_at(x,y), right_click_at(x,y), double_click_at(x,y), move_mouse(x,y), drag_mouse(fx,fy,tx,ty), get_mouse_position, get_screen_size
VOLUME: volume_up, volume_down, mute_volume
BROWSER: open_website, search_web, clear_chrome_history, clear_edge_history
FILES: empty_recycle_bin, open_folder, create_folder, delete_file
MEDIA: play_pause_media, next_track, previous_track, play_music_from_folder
TIMERS: set_timer, set_reminder
CLIPBOARD: get_clipboard, set_clipboard
MISC: get_current_time, run_command, get_commands
""".strip()