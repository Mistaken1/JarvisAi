from google.genai import types
import AI_functions

# ─────────────────────────────────────────────
# FUNCTIONS MAP
# ─────────────────────────────────────────────

FUNCTIONS = {
    # App Control
    "open_app":             AI_functions.open_app,
    "close_app":            AI_functions.close_app,
    "list_running_apps":    AI_functions.list_running_apps,

    # System
    "shutdown_computer":    AI_functions.shutdown_computer,
    "restart_computer":     AI_functions.restart_computer,
    "sleep_computer":       AI_functions.sleep_computer,
    "lock_computer":        AI_functions.lock_computer,
    "get_battery_status":   AI_functions.get_battery_status,
    "get_cpu_usage":        AI_functions.get_cpu_usage,
    "get_ram_usage":        AI_functions.get_ram_usage,

    # Screen / Input
    "take_screenshot":      AI_functions.take_screenshot,
    "type_text":            AI_functions.type_text,
    "press_key":            AI_functions.press_key,
    "hotkey":               AI_functions.hotkey,
    "scroll_up":            AI_functions.scroll_up,
    "scroll_down":          AI_functions.scroll_down,
    "zoom_in":              AI_functions.zoom_in,
    "zoom_out":             AI_functions.zoom_out,
    "analyze_screen":       AI_functions.analyze_screen,

    # Mouse Control
    "click_at":             AI_functions.click_at,
    "right_click_at":       AI_functions.right_click_at,
    "double_click_at":      AI_functions.double_click_at,
    "move_mouse":           AI_functions.move_mouse,
    "drag_mouse":           AI_functions.drag_mouse,
    "get_mouse_position":   AI_functions.get_mouse_position,
    "get_screen_size":      AI_functions.get_screen_size,

    # Volume
    "volume_up":            AI_functions.volume_up,
    "volume_down":          AI_functions.volume_down,
    "mute_volume":          AI_functions.mute_volume,

    # Browser / Web
    "open_website":         AI_functions.open_website,
    "search_web":           AI_functions.search_web,
    "clear_chrome_history": AI_functions.clear_chrome_history,
    "clear_edge_history":   AI_functions.clear_edge_history,

    # Files & Folders
    "empty_recycle_bin":    AI_functions.empty_recycle_bin,
    "open_folder":          AI_functions.open_folder,
    "create_folder":        AI_functions.create_folder,
    "delete_file":          AI_functions.delete_file,

    # Music / Media
    "play_pause_media":     AI_functions.play_pause_media,
    "next_track":           AI_functions.next_track,
    "previous_track":       AI_functions.previous_track,
    "play_music_from_folder": AI_functions.play_music_from_folder,

    # Timers & Reminders
    "set_timer":            AI_functions.set_timer,
    "set_reminder":         AI_functions.set_reminder,

    # Clipboard
    "get_clipboard":        AI_functions.get_clipboard,
    "set_clipboard":        AI_functions.set_clipboard,

    # Misc
    "get_current_time":     AI_functions.get_current_time,
    "run_command":          AI_functions.run_command,
    "get_commands":         AI_functions.get_commands,
}

# ─────────────────────────────────────────────
# DECLARATIONS
# ─────────────────────────────────────────────

declarations = [

    # ── App Control ──
    {
        "name": "open_app",
        "description": "Opens an application on the computer by name or file path.",
        "parameters": {
            "type": "object",
            "properties": {
                "app_name": {"type": "string", "description": "Name or full path of the app to open."}
            },
            "required": ["app_name"]
        }
    },
    {
        "name": "close_app",
        "description": "Closes a running application by process name.",
        "parameters": {
            "type": "object",
            "properties": {
                "app_name": {"type": "string", "description": "Process name to close (e.g. 'chrome', 'notepad')."}
            },
            "required": ["app_name"]
        }
    },
    {
        "name": "list_running_apps",
        "description": "Returns a list of all currently running processes.",
        "parameters": {"type": "object", "properties": {}, "required": []}
    },

    # ── System ──
    {
        "name": "shutdown_computer",
        "description": "Shuts down the computer in 5 seconds.",
        "parameters": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "restart_computer",
        "description": "Restarts the computer in 5 seconds.",
        "parameters": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "sleep_computer",
        "description": "Puts the computer to sleep.",
        "parameters": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "lock_computer",
        "description": "Locks the computer screen.",
        "parameters": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "get_battery_status",
        "description": "Returns current battery percentage and charging status.",
        "parameters": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "get_cpu_usage",
        "description": "Returns current CPU usage percentage.",
        "parameters": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "get_ram_usage",
        "description": "Returns current RAM usage.",
        "parameters": {"type": "object", "properties": {}, "required": []}
    },

    # ── Screen / Input ──
    {
        "name": "take_screenshot",
        "description": "Takes a screenshot and saves it to the Pictures folder.",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "description": "Optional filename. Defaults to a timestamped name."}
            },
            "required": []
        }
    },
    {
        "name": "analyze_screen",
        "description": "Takes a screenshot of the current screen and answers a question about what's on it. Use this whenever the user asks what's on screen, what's open, or to interact based on what they can see.",
        "parameters": {
            "type": "object",
            "properties": {
                "question": {"type": "string", "description": "The question to answer about the screen."}
            },
            "required": ["question"]
        }
    },
    {
        "name": "type_text",
        "description": "Types text at the current cursor position.",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Text to type."}
            },
            "required": ["text"]
        }
    },
    {
        "name": "press_key",
        "description": "Presses a single keyboard key (e.g. 'enter', 'escape', 'tab', 'f5').",
        "parameters": {
            "type": "object",
            "properties": {
                "key": {"type": "string", "description": "Key to press."}
            },
            "required": ["key"]
        }
    },
    {
        "name": "hotkey",
        "description": "Presses a keyboard shortcut combination. Pass keys as comma-separated string (e.g. 'ctrl,c' for copy, 'ctrl,shift,t' to reopen tab, 'alt,f4' to close).",
        "parameters": {
            "type": "object",
            "properties": {
                "keys": {"type": "string", "description": "Comma-separated keys to hold simultaneously (e.g. 'ctrl,c', 'ctrl,alt,delete', 'win,d')."}
            },
            "required": ["keys"]
        }
    },
    {
        "name": "scroll_up",
        "description": "Scrolls the screen up.",
        "parameters": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "scroll_down",
        "description": "Scrolls the screen down.",
        "parameters": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "zoom_in",
        "description": "Zooms in using Ctrl++.",
        "parameters": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "zoom_out",
        "description": "Zooms out using Ctrl+-.",
        "parameters": {"type": "object", "properties": {}, "required": []}
    },

    # ── Mouse Control ──
    {
        "name": "click_at",
        "description": "Clicks the mouse at a specific screen coordinate. Use analyze_screen first to find coordinates if needed.",
        "parameters": {
            "type": "object",
            "properties": {
                "x": {"type": "integer", "description": "Horizontal pixel coordinate."},
                "y": {"type": "integer", "description": "Vertical pixel coordinate."}
            },
            "required": ["x", "y"]
        }
    },
    {
        "name": "right_click_at",
        "description": "Right-clicks at a specific screen coordinate.",
        "parameters": {
            "type": "object",
            "properties": {
                "x": {"type": "integer", "description": "Horizontal pixel coordinate."},
                "y": {"type": "integer", "description": "Vertical pixel coordinate."}
            },
            "required": ["x", "y"]
        }
    },
    {
        "name": "double_click_at",
        "description": "Double-clicks at a specific screen coordinate.",
        "parameters": {
            "type": "object",
            "properties": {
                "x": {"type": "integer", "description": "Horizontal pixel coordinate."},
                "y": {"type": "integer", "description": "Vertical pixel coordinate."}
            },
            "required": ["x", "y"]
        }
    },
    {
        "name": "move_mouse",
        "description": "Moves the mouse cursor to a screen coordinate without clicking.",
        "parameters": {
            "type": "object",
            "properties": {
                "x": {"type": "integer", "description": "Horizontal pixel coordinate."},
                "y": {"type": "integer", "description": "Vertical pixel coordinate."}
            },
            "required": ["x", "y"]
        }
    },
    {
        "name": "drag_mouse",
        "description": "Clicks and drags from one screen coordinate to another.",
        "parameters": {
            "type": "object",
            "properties": {
                "from_x": {"type": "integer", "description": "Start X coordinate."},
                "from_y": {"type": "integer", "description": "Start Y coordinate."},
                "to_x": {"type": "integer", "description": "End X coordinate."},
                "to_y": {"type": "integer", "description": "End Y coordinate."}
            },
            "required": ["from_x", "from_y", "to_x", "to_y"]
        }
    },
    {
        "name": "get_mouse_position",
        "description": "Returns the current mouse cursor position on screen.",
        "parameters": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "get_screen_size",
        "description": "Returns the screen resolution (width x height in pixels).",
        "parameters": {"type": "object", "properties": {}, "required": []}
    },

    # ── Volume ──
    {
        "name": "volume_up",
        "description": "Increases the system volume.",
        "parameters": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "volume_down",
        "description": "Decreases the system volume.",
        "parameters": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "mute_volume",
        "description": "Mutes or unmutes the system volume.",
        "parameters": {"type": "object", "properties": {}, "required": []}
    },

    # ── Browser / Web ──
    {
        "name": "open_website",
        "description": "Opens a URL in the default browser.",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "URL to open (e.g. 'youtube.com')."}
            },
            "required": ["url"]
        }
    },
    {
        "name": "search_web",
        "description": "Searches Google for a query and opens results in the browser.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query."}
            },
            "required": ["query"]
        }
    },
    {
        "name": "clear_chrome_history",
        "description": "Clears Google Chrome browsing history. Chrome must be closed first.",
        "parameters": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "clear_edge_history",
        "description": "Clears Microsoft Edge browsing history. Edge must be closed first.",
        "parameters": {"type": "object", "properties": {}, "required": []}
    },

    # ── Files & Folders ──
    {
        "name": "empty_recycle_bin",
        "description": "Empties the Windows recycle bin.",
        "parameters": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "open_folder",
        "description": "Opens a folder in File Explorer.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Folder path to open."}
            },
            "required": ["path"]
        }
    },
    {
        "name": "create_folder",
        "description": "Creates a new folder at the specified path.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Full path of the folder to create."}
            },
            "required": ["path"]
        }
    },
    {
        "name": "delete_file",
        "description": "Permanently deletes a file.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Full path of the file to delete."}
            },
            "required": ["path"]
        }
    },

    # ── Music / Media ──
    {
        "name": "play_pause_media",
        "description": "Plays or pauses currently playing media.",
        "parameters": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "next_track",
        "description": "Skips to the next media track.",
        "parameters": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "previous_track",
        "description": "Goes back to the previous media track.",
        "parameters": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "play_music_from_folder",
        "description": "Plays the first music file found in a folder.",
        "parameters": {
            "type": "object",
            "properties": {
                "folder": {"type": "string", "description": "Optional folder path. Defaults to ~/Music."}
            },
            "required": []
        }
    },

    # ── Timers & Reminders ──
    {
        "name": "set_timer",
        "description": "Sets a countdown timer that sends a Windows notification when done.",
        "parameters": {
            "type": "object",
            "properties": {
                "seconds": {"type": "integer", "description": "Number of seconds for the timer."}
            },
            "required": ["seconds"]
        }
    },
    {
        "name": "set_reminder",
        "description": "Sets a reminder that appears as a notification after a delay.",
        "parameters": {
            "type": "object",
            "properties": {
                "message": {"type": "string", "description": "Reminder message."},
                "seconds": {"type": "integer", "description": "Seconds from now to show the reminder."}
            },
            "required": ["message", "seconds"]
        }
    },

    # ── Clipboard ──
    {
        "name": "get_clipboard",
        "description": "Returns the current clipboard contents.",
        "parameters": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "set_clipboard",
        "description": "Copies text to the clipboard.",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Text to copy."}
            },
            "required": ["text"]
        }
    },

    # ── Misc ──
    {
        "name": "get_current_time",
        "description": "Returns the current date and time.",
        "parameters": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "run_command",
        "description": "Runs a shell/terminal command and returns output. Use with caution.",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "Shell command to run."}
            },
            "required": ["command"]
        }
    },
    {
        "name": "get_commands",
        "description": "Returns a list of all available functions.",
        "parameters": {"type": "object", "properties": {}, "required": []}
    },
]

# ─────────────────────────────────────────────
# TOOLS OBJECT
# ─────────────────────────────────────────────

tools = types.Tool(function_declarations=declarations)