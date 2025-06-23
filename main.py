import tkinter as tk
import os
import datetime
import ctypes
from stickynotes import *

if __name__ == "__main__":
    if not os.path.exists("notes"):
        os.makedirs("notes")

    root = tk.Tk()
    root.iconbitmap("asset/icon.ico")
    root.geometry("0x0+0+0")
    root.overrideredirect(True)

    # Fix taskbar icon trên Windows
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(u"my.sticky.note")
    except:
        pass

    json_files = [f for f in os.listdir("notes") if f.endswith(".json")]
    if not json_files:
        now = datetime.datetime.now().isoformat(timespec='seconds')
        file_name = "notes/note1.json"
        data = {
            "id": 1,
            "title": "Ghi chú",
            "content": "",
            "color": "#FFC107",
            "last_modified": now
        }
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    for file in os.listdir("notes"):
        if file.endswith(".json"):
            full_path = os.path.join("notes", file)
            note_window = tk.Toplevel(root)
            note_window.resizable(False, False)
            note_window.maxsize(None, None)
            note_window.overrideredirect(True)
            note_window.iconbitmap("asset/icon.ico")
            StickyNote(note_window, full_path)

    root.mainloop()
