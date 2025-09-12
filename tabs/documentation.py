# tabs/documentation.py
import tkinter as tk
from tkinter import ttk
import webbrowser

class DocumentationTab(ttk.Frame):
    """
    A tab to display a collection of documentation links.
    """
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.root = None
        self.status_bar = None

        # A structured dictionary to hold all documentation links by category
        self.link_categories = {
            "General Guides": [
                ("General Modding", "https://docs.google.com/document/d/1usRsCq6gNF1viIhVWHQUCXkDR9Wqbw6vU3jAyardrf0/edit?tab=t.0"),
                ("Skeletal Mesh Replacement", "https://modworkshop.net/mod/49737")
            ],
            "Audio Modding": [
                ("Audio Replacements without Events", "https://docs.google.com/document/d/1M7aicj57HXp92XPSMSg4KyEDkoc3iNzshaA18rIsUXw/edit?tab=t.0#heading=h.qr0hstskc95i"),
                ("Audio Replacements with Events", "https://docs.google.com/document/d/1Q8m5Odwhwdyc64jsPJ6byp7sKSdzEArkRDFmLfrpQ5s/edit?tab=t.0#heading=h.1br8tw1ezfrh"),
                ("Custom Heist Tracks", "https://docs.google.com/document/d/1f6ComClQIJrvrdo5Yu-VmFC7ykKrs_8EyKiMkRRfbhc/edit?tab=t.0#heading=h.wjyyevobb0m0"),
                ("PAYDAY 3 Audio Modder","https://modworkshop.net/mod/51045"),
            ],
            "Visual & Asset Modding": [
                ("Sticker Replacement", "https://docs.google.com/document/d/15fxhIUzrfkTXYg3EWFLXXid4LNeRUCzecS9SYLJEPwo/edit?usp=sharing"),
                ("Loot Bag Replacement / Body Pillows", "https://docs.google.com/document/d/1PAog1l_E16WBXM8-AJXv2zYaBSpfCAAZ-LvvesOEZ0s/edit?usp=sharing"),
                ("Unique Loot Bags", "https://docs.google.com/document/d/1agtZ2s6NIzRPFCeedPJpXMmlVjrDeO7z1OZNOvKhJl8/edit?usp=sharing"),
            ],
            "Heist Modding": [
                ("Custom Heists", "https://docs.google.com/document/d/1mIFz7MGtSIbDj4bkEdGb8MZJA5ezYFwFBxlk6A62EYU/edit?tab=t.0#heading=h.l5a949mgy9gr"),
                ("Custom Heist Video Tutorials", "https://youtube.com/playlist?list=PLRSASA7UrjTvrBML_cbcwKFE6ZnZkRf-C&si=bdRbA17Utq9sP1tC"),
            ],
            "ID Spreadsheets & Tools": [
                ("Wwise Media IDs", "https://docs.google.com/spreadsheets/d/1j_krhOGUE0zl-TiMF9depNCeyE89RNxquWfKDLk6vJw/edit?gid=0#gid=0"),
                ("Wwise Localized Media IDs", "https://docs.google.com/spreadsheets/d/1LVGv56lxQjI10vf0TdGN97Bq1qJC9FNbU0CyUa4tpdU/edit?gid=0#gid=0"),
                ("Gun IDs", "https://docs.google.com/spreadsheets/d/1Me4OK7pksZzkMfCuIqKW-27bGTxro_2q372fwUQYnTY/edit?gid=0#gid=0"),
                ("Female Heister IDs", "https://docs.google.com/spreadsheets/d/16UYUj-X1q94hR0AqaY3PvmlODPEtNKdbOk76D0locmE/edit?usp=sharing"),
                ("Male Heister IDs", "https://docs.google.com/spreadsheets/d/1BwiYpH1KfwB6C6uDalqYCJXt2HOF75H5CQVCEZ_jbuk/edit?usp=sharing"),
                ("PAYDAY 3 Unreal Locres Editor", "https://modworkshop.net/mod/48158")
            ]
        }

        self.create_widgets()

    def create_widgets(self):
        # A framed "glass box" to contain the content with styling
        glass_box = ttk.Frame(self, style='TFrame', padding=(15, 15), relief='groove', borderwidth=2)
        glass_box.pack(expand=True, fill="both", padx=10, pady=10)

        # Scrolled frame for categories
        canvas = tk.Canvas(glass_box, bg='#1a1a1a', highlightthickness=0)
        scrollbar = ttk.Scrollbar(glass_box, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='TFrame', padding=(10, 10))

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Configure grid for two columns to better utilize horizontal space
        scrollable_frame.grid_columnconfigure(0, weight=1, uniform="group1")
        scrollable_frame.grid_columnconfigure(1, weight=1, uniform="group1")

        # Loop through categories and create frames and buttons
        for i, (category, links) in enumerate(self.link_categories.items()):
            row, col = divmod(i, 2)

            # Create a bordered frame for the category
            category_frame = ttk.Frame(scrollable_frame, style='TFrame', padding=(10, 10), relief='groove', borderwidth=1)
            category_frame.grid(row=row, column=col, sticky="nsew", padx=5, pady=(0, 15))

            # Category title
            title_label = ttk.Label(category_frame, text=category, style='TLabel', font=("Helvetica", 14, "bold"))
            title_label.pack(pady=(0, 10), anchor='w')

            # Create and place buttons for each link
            for name, url in links:
                button = ttk.Button(category_frame, text=name, command=lambda u=url: self.open_link(u), style='TButton')
                button.pack(pady=4, fill='x', expand=True)

    def open_link(self, url):
        """
        Opens a URL in the default web browser and updates the status bar.
        """
        try:
            webbrowser.open_new(url)
            if self.status_bar:
                self.status_bar.config(text=f"Opened documentation link: {url}")
        except Exception as e:
            if self.status_bar:
                self.status_bar.config(text=f"Error opening link: {e}")
