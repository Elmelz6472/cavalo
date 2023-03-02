import os
import subprocess
import tkinter as tk
from tkinter import filedialog


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Execute Python Script")
        self.master.geometry("400x350")
        self.master.resizable(True, True)
        self.pack()
        self.create_widgets()
        self.process = None

    def create_widgets(self):
        self.keyword_label = tk.Label(
            self, text="Keyword argument:", font=("Helvetica", 12)
        )
        self.keyword_label.pack(side="top", pady=10)
        self.keyword_entry = tk.Entry(self, font=("Helvetica", 12), width=30)
        self.keyword_entry.pack(side="top", padx=10, pady=5)

        self.location_label = tk.Label(
            self, text="Location argument:", font=("Helvetica", 12)
        )
        self.location_label.pack(side="top", pady=10)
        self.location_entry = tk.Entry(self, font=("Helvetica", 12), width=30)
        self.location_entry.pack(side="top", padx=10, pady=5)

        self.depth_label = tk.Label(
            self, text="Depth argument:", font=("Helvetica", 12)
        )
        self.depth_label.pack(side="top", pady=10)
        self.depth_entry = tk.Entry(self, font=("Helvetica", 12), width=30)
        self.depth_entry.pack(side="top", padx=10, pady=5)

        self.select_button = tk.Button(
            self,
            text="Select Script File",
            width=20,
            height=2,
            font=("Helvetica", 12, "bold"),
            command=self.select_script_file,
        )
        self.select_button.pack(side="top", padx=10, pady=10)

        self.run_button = tk.Button(
            self,
            text="Run Python Script",
            width=20,
            height=2,
            font=("Helvetica", 12, "bold"),
            state="disabled",
            command=self.run_script,
        )
        self.run_button.pack(side="left", padx=10, pady=10)

        self.cancel_button = tk.Button(
            self,
            text="Cancel Script",
            width=20,
            height=2,
            font=("Helvetica", 12, "bold"),
            state="disabled",
            command=self.cancel_script,
        )
        self.cancel_button.pack(side="right", padx=10, pady=10)

    def select_script_file(self):
        self.script_file = filedialog.askopenfilename(
            title="Select Script File",
            filetypes=[("Python Files", "*.py"), ("All Files", "*.*")],
        )
        if self.script_file:
            self.run_button.config(state="normal")

            # Set the script filename as the text of the "Select Script File" button
            self.select_button.configure(text=os.path.basename(self.script_file))

    def run_script(self):
        command = [
            "python",
            self.script_file,
            self.keyword_entry.get(),
            self.location_entry.get(),
            self.depth_entry.get(),
        ]
        self.process = subprocess.Popen(command)
        self.run_button.config(state="disabled")
        self.cancel_button.config(state="normal")

    def cancel_script(self):
        if self.process:
            self.process.kill()
            self.process = None
            self.run_button.config(state="normal")
            self.cancel_button.config(state="disabled")


root = tk.Tk()
app = Application(master=root)
app.mainloop()
