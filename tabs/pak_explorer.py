# tabs/pak_explorer.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import zipfile

class PakExplorerTab(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.status_bar = None
        self.create_widgets()

    def create_widgets(self):
        # A framed "glass box" to contain the content
        glass_box = ttk.Frame(self, style='TFrame', padding=(15, 15), relief='groove', borderwidth=2)
        glass_box.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Frame for folder selection and buttons
        pak_frame = ttk.Frame(glass_box, style='TFrame')
        pak_frame.pack(fill='x', pady=5)
        
        ttk.Label(pak_frame, text="Select .PAK File:", style='TLabel').pack(side='left', padx=(0, 5))
        
        self.pak_file_path_var = tk.StringVar()
        self.pak_file_path_entry = ttk.Entry(pak_frame, textvariable=self.pak_file_path_var, width=50)
        self.pak_file_path_entry.pack(side='left', expand=True, fill='x', padx=(0, 5))
        
        browse_button = ttk.Button(pak_frame, text="Browse", command=self.browse_pak_file, width=15)
        browse_button.pack(side='left')
        
        # Frame for file tree and scrollbar
        tree_frame = ttk.Frame(glass_box, style='TFrame')
        tree_frame.pack(expand=True, fill='both', pady=10)

        self.tree = ttk.Treeview(tree_frame, columns=('Size'), show='tree headings')
        self.tree.heading('#0', text='File Path')
        self.tree.heading('Size', text='Size (Bytes)')
        self.tree.pack(side='left', expand=True, fill='both')

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        ttk.Label(glass_box, text="NOTE: This is a simulated PAK viewer for demonstration. PAK files are not standard zip files and require specific libraries (like Python's `unpak` or `pyue4pak`) to be fully explored.", style='TLabel', font=("Helvetica", 8), foreground="#999999").pack(pady=10)

    def browse_pak_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PAK files", "*.pak")])
        if file_path:
            self.pak_file_path_var.set(file_path)
            self.update_status(f"Selected: {os.path.basename(file_path)}")
            self.load_pak_contents(file_path)

    def load_pak_contents(self, file_path):
        self.tree.delete(*self.tree.get_children())
        
        if not os.path.exists(file_path):
            messagebox.showerror("Error", "Selected file does not exist.")
            self.update_status("Error: File not found.")
            return

        # Simplified for demonstration. Real PAKs require a specialized library.
        # We will treat it as a zip file to show a tree structure, even though it's not.
        try:
            with zipfile.ZipFile(file_path, 'r') as pak_zip:
                for item in pak_zip.infolist():
                    self.tree.insert('', 'end', text=item.filename, values=(item.file_size,))
            self.update_status(f"Successfully loaded contents of {os.path.basename(file_path)}")
        except zipfile.BadZipFile:
            # If it's not a zip file (which it won't be), display a clear message
            self.tree.insert('', 'end', text=f"File is not a valid zip archive. A specialized PAK parser is required.")
            self.update_status("Error: Not a valid PAK file format.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while reading the PAK file: {e}")
            self.update_status("Error loading PAK file.")

    def update_status(self, message):
        if self.status_bar:
            self.status_bar.config(text=message)
        self.root.update_idletasks()
