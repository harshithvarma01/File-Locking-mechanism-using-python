import tkinter as tk
from tkinter import messagebox, filedialog
import os
import msvcrt

class FileLockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Locking Mechanism (Windows)")
        self.root.geometry("500x350")
        
        self.files = []
        self.locked_files = set()

        # Create a Label
        self.label = tk.Label(root, text="File Locking Mechanism", font=("Arial", 18, "bold"))
        self.label.pack(pady=20)

        # Select Files Button
        self.select_button = tk.Button(root, text="Select Files", font=("Arial", 14), command=self.select_files)
        self.select_button.pack(pady=10)

        # Lock Files Button
        self.lock_button = tk.Button(root, text="Lock Files", font=("Arial", 14), command=self.lock_files, state="disabled")
        self.lock_button.pack(pady=10)

        # Unlock Files Button
        self.unlock_button = tk.Button(root, text="Unlock Files", font=("Arial", 14), command=self.unlock_files, state="disabled")
        self.unlock_button.pack(pady=10)

        # File Status Label
        self.status_label = tk.Label(root, text="File Status: Not Selected", font=("Arial", 12))
        self.status_label.pack(pady=20)

    def select_files(self):
        # Allow user to select multiple files
        files = filedialog.askopenfilenames(title="Select Files")
        if files:
            self.files = files
            self.status_label.config(text=f"Selected Files: {', '.join(os.path.basename(f) for f in files)}")
            self.lock_button.config(state="normal")
            self.unlock_button.config(state="normal")

    def lock_files(self):
        if not self.files:
            messagebox.showwarning("Error", "No files selected.")
            return

        for file in self.files:
            try:
                # Lock the file by renaming it to indicate it's locked
                locked_file = file + ".locked"
                if not os.path.exists(locked_file):
                    os.rename(file, locked_file)
                    self.locked_files.add(file)
                    messagebox.showinfo("File Locked", f"File {file} is now locked.")
                else:
                    messagebox.showwarning("File Locked", f"File {file} is already locked.")
            except IOError:
                messagebox.showerror("Error", f"Unable to lock the file: {file}")
        self.files = []  # Clear file selection after locking
        self.status_label.config(text="File Status: Files Locked")

    def unlock_files(self):
        if not self.locked_files:
            messagebox.showwarning("Error", "No locked files to unlock.")
            return

        for file in list(self.locked_files):
            try:
                # Unlock the file by renaming it back to the original name
                locked_file = file + ".locked"
                if os.path.exists(locked_file):
                    os.rename(locked_file, file)
                    self.locked_files.remove(file)
                    messagebox.showinfo("File Unlocked", f"File {file} is now unlocked.")
                else:
                    messagebox.showwarning("File Unlocked", f"File {file} is not locked.")
            except IOError:
                messagebox.showerror("Error", f"Unable to unlock the file: {file}")
        self.status_label.config(text="File Status: Files Unlocked")

# Main
if __name__ == "__main__":
    root = tk.Tk()
    app = FileLockApp(root)
    root.mainloop()

