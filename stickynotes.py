import tkinter as tk
import json
import os
import random
import datetime

Color = {
    "yellow": "#FFC107",
    "blue":"#0B1D51",
    "black":"#2b2b2b",
    "pink": "#FFAAAA",
    "green": "#4E71FF",
}

class StickyNote:
    def __init__(self, root ,file_name):
        self.root = root
        self.color = Color["yellow"]
        self.text_color = "#F2F2F2"
        self.file_name = file_name
        self.title_text = ""
        self.title_lable = None
        self.area_text = None
        self.tool_bar = None
        self.toolbar()
        self.area_status = True
        self.textarea()
        self.loadfile()
        self.root.geometry("350x350+100+100")
        self.root.configure(bg="#2b2b2b")
        self.root.attributes("-topmost", True)
        self.setting_frame = None
        self.button_remove = None
        self.button_list = None

    def toolbar(self):
        self.tool_bar = tk.Frame(self.root, bg=self.color, height=34, cursor="hand2")
        self.tool_bar.pack(side="top", fill="x")
        self.tool_bar.pack_propagate(False)

        self.tool_bar.bind("<Button-1>", self.start_move)
        self.tool_bar.bind("<B1-Motion>", self.do_move)


        button_add = tk.Button(self.tool_bar, text="➕", command=self.add, bd=0, font=("Arial", 12), bg=self.color,
                                 fg=self.text_color, activebackground=self.color)
        button_add.pack(side="left", padx=5)

        self.title_lable = tk.Label(self.tool_bar, text=self.title_text,font=("Arial", 11), bg=self.color, height=34, cursor="hand2",fg=self.text_color)
        self.title_lable.pack(side="left", fill="x")

        self.root.bind("<Button-1>", self.start_move)

        button_close = tk.Button(self.tool_bar, text="❌", command=self.exit_app, bd=0, font=("Arial", 12), bg=self.color,
                                 fg=self.text_color, activebackground=self.color)
        button_close.pack(side="right", padx=5)
        # Nút thực hiện
        button_setting = tk.Button(self.tool_bar, text="⚙️", command=self.setting, bd=0, font=("Arial", 12), bg=self.color,
                                 fg=self.text_color, activebackground=self.color)
        button_setting.pack(side="right", padx=5)
        print("Đã tạo tool bar...")
    def textarea(self):
       self.area_text = tk.Text(
                self.root,
                font=("Segoe UI", 12),
                fg="#ffffff",
                bg="#2b2b2b",
                insertbackground="#ffffff",
                selectbackground=self.color,  # màu nền khi chọn
                selectforeground="#ffffff",  # màu chữ khi chọn
                bd=0,
                highlightthickness=0,
                wrap="word"
            )
       self.area_text.pack(padx=5, pady=5)
       self.area_text.bind("<<Modified>>", self.auto_save)
       print("Đã tạo text area...")

    def auto_save(self,event=None):
        content = self.area_text.get("1.0", tk.END)
        data = {
          "id": 1,
          "title": self.title_text,
          "content": content,
          "color":self.color,
          "last_modified": "2025-06-22T20:00:00"
        }
        with open(self.file_name, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        self.area_text.edit_modified(False)


    def start_move(self, event):
        self.x = event.x
        self.y = event.y
    def do_move(self, event):
        x = self.root.winfo_pointerx() - self.x
        y = self.root.winfo_pointery() - self.y
        self.root.geometry(f"+{x}+{y}")

    def exit_app(self):
        if self.area_status:
            content = self.area_text.get("1.0", "end-1c").strip()
            if len(content) == 0:
                os.remove(os.path.join(self.file_name))
                self.root.destroy()
            else:
                self.root.destroy()


    def add(self):
        now = datetime.datetime.now().isoformat(timespec='seconds')
        new_root = tk.Toplevel()
        new_root.resizable(False, False)
        new_root.maxsize(None, None)
        new_root.overrideredirect(True)
        new_root.geometry("350x350+100+100")

        id = self.randomid()
        count = len([f for f in os.listdir("notes/") if f.endswith(".json")]) + 1
        new_file_name = f"notes/note{id}.json"
        data = {
            "id": f"{count}" ,
            "title": f"Ghi chú",
            "content": "",
            "color": Color["yellow"],
            "last_modified": now
        }

        # Lưu file JSON
        with open(new_file_name, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        # Mở ghi chú mới
        StickyNote(new_root, new_file_name)
    def randomid(self):
        while True:
            id = random.randint(0, 10000)
            file_path = os.path.join("notes", f"note{id}.json")
            if not os.path.exists(file_path):
                return id
    def setting(self):
            if self.area_status:
                self.area_status = False
                if self.area_text:
                    self.area_text.destroy()
                    self.area_text = None

                    self.setting_frame = tk.Frame(self.root, bg="#FFFCFB", height=80 )
                    self.setting_frame.pack(fill="x")

                    btn1 = tk.Button(self.setting_frame,command=lambda: self.change_color_toolbar("#FFC107"),fg="white" , bg="#FFC107" , width = 12 , border = 0 , cursor="hand2", activebackground="#2b2b2b")
                    btn1.pack(side=tk.LEFT, padx=0)

                    btn2 = tk.Button(self.setting_frame,command=lambda: self.change_color_toolbar("#0B1D51"), fg="white", bg="#0B1D51", width=12, border=0 ,cursor="hand2", activebackground="#2b2b2b")
                    btn2.pack(side=tk.LEFT, padx=0)

                    btn3 = tk.Button(self.setting_frame, command=lambda: self.change_color_toolbar(Color["pink"]),fg="white", bg=Color["pink"], width=12, border=0, cursor="hand2", activebackground="#2b2b2b")
                    btn3.pack(side=tk.LEFT, padx=0)

                    btn4 = tk.Button(self.setting_frame,command=lambda: self.change_color_toolbar(Color["green"]), fg="white", bg=Color["green"], width=12, border=0, cursor="hand2", activebackground="#2b2b2b")
                    btn4.pack(side=tk.LEFT, padx=0)

                    self.button_list =  tk.Button(self.root,  text=" ☰    Danh sách ghi chú", bg="#393E46", height=2 , fg="white", cursor="hand2", activebackground="#2b2b2b" , activeforeground="white" , border=0 ,font=("Arial", 11) )
                    self.button_list.pack(fill="x")

                    self.button_remove = tk.Button(self.root,  text="🗑️Xóa ghi chú", bg="#393E46", height=2 , fg="white", cursor="hand2", activebackground="#2b2b2b" , activeforeground="white" , border=0 ,font=("Arial", 11) , command=self.remove_note )
                    self.button_remove.pack(fill="x")

            else:
                self.area_status = True
                if self.setting_frame:
                    self.setting_frame.destroy()
                    self.button_remove.destroy()
                    self.button_list.destroy()
                    self.setting_frame = None
                    self.button_remove = None
                    self.button_list = None
                self.textarea()
                content = self.getContent()
                self.area_text.insert("1.0",content)
    def change_color_toolbar(self, new_color):
        self.color = new_color
        self.tool_bar.configure(bg=new_color)
        self.changebgitems(new_color)
    def changebgitems(self,color):
        for widget in self.tool_bar.winfo_children():
            if isinstance(widget, tk.Button):
                widget.configure(bg=color, activebackground=color, fg=self.text_color)
            elif isinstance(widget, tk.Label):
                widget.configure(bg=color, activebackground=color, fg=self.text_color)
    def loadfile(self):
        if not os.path.exists(self.file_name):
            return
        with open(self.file_name, "r", encoding="utf-8") as file:
            notes_data = json.load(file)
            self.title_text = notes_data.get("title", "")
            self.title_lable.config(text=self.title_text)
            self.area_text.insert("1.0", notes_data["content"])
            self.color = notes_data.get("color", "")
            self.tool_bar.configure(bg=notes_data["color"])
            self.changebgitems(notes_data["color"])
    def getContent(self):
        if not os.path.exists(self.file_name):
            return
        with open(self.file_name, "r", encoding="utf-8") as file:
            notes_data = json.load(file)
            return notes_data.get("content", "")
    def remove_note(self):
        os.remove(self.file_name)
        self.root.destroy()
