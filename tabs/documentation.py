# tabs/documentation.py
import tkinter as tk
from tkinter import ttk, Text

class DocumentationTab(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        glass_box = ttk.Frame(self, style='TFrame', padding=(15, 15), relief='groove', borderwidth=2)
        glass_box.pack(expand=True, fill="both", padx=10, pady=10)
        
        ttk.Label(glass_box, text="Documentation", font=("Helvetica", 16, "bold"), style='TLabel').pack(pady=5)
        
        doc_text_widget = Text(glass_box, wrap='word', height=10, bg="#1a1a1a", fg="white", font=("Helvetica", 11), padx=10, pady=10, relief='flat', borderwidth=0)
        doc_text_widget.pack(fill='both', expand=True)
        doc_text_widget.insert(tk.END, "Content for this tab will be added later. This section will contain instructions and usage information for the tool.")
        doc_text_widget.configure(state='disabled')