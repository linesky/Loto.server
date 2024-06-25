
import tkinter as tk
from tkinter import scrolledtext
import os

class PostItApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Post-it")
        self.root.configure(bg='yellow')

        self.text_area = scrolledtext.ScrolledText(root, width=40, height=20, bg='white')
        self.text_area.pack(padx=10, pady=10)

        self.load_notes()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_notes(self):
        if os.path.exists("postit.ini"):
            with open("postit.ini", "r") as file:
                content = file.read()
                self.text_area.insert(tk.END, content)

    def save_notes(self):
        with open("postit.ini", "w") as file:
            content = self.text_area.get(1.0, tk.END)
            file.write(content.strip())

    def on_closing(self):
        self.save_notes()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PostItApp(root)
    root.mainloop()
