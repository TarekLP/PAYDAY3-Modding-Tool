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

        self.create_widgets()

    def create_widgets(self):
        # A framed "glass box" to contain the content with styling
        glass_box = ttk.Frame(self, style='TFrame', padding=(15, 15), relief='groove', borderwidth=2)
        glass_box.pack(expand=True, fill="both", padx=10, pady=10)

        # Configure the grid on the glass_box to manage left and right sections
        glass_box.grid_columnconfigure(0, weight=1)  # Left column for links
        glass_box.grid_columnconfigure(1, weight=2)  # Right column for video button
        glass_box.grid_rowconfigure(0, weight=1)

        # Frame for the documentation buttons, placed on the left
        left_frame = ttk.Frame(glass_box, style='TFrame')
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # This inner frame will vertically center the buttons
        button_frame = ttk.Frame(left_frame, style='TFrame')
        button_frame.pack(expand=True)
        
        # --- Documentation Links Section ---
        # Add the "Guides" header
        ttk.Label(button_frame, text="Guides", font=("Helvetica", 14, "bold"), style='TLabel').pack(pady=(0, 10))

        documentation_links = [
            ("General Modding", "https://docs.google.com/document/d/1usRsCq6gNF1viIhVWHQUCXkDR9Wqbw6vU3jAyardrf0/edit?tab=t.0"),
            ("Custom Heists", "https://docs.google.com/document/d/1mIFz7MGtSIbDj4bkEdGb8MZJA5ezYFwFBxlk6A62EYU/edit?tab=t.0#heading=h.l5a949mgy9gr"),
            ("Audio Replacements without Events", "https://docs.google.com/document/d/1M7aicj57HXp92XPSMSg4KyEDkoc3iNzshaA18rIsUXw/edit?tab=t.0#heading=h.qr0hstskc95i"),
            ("Audio Replacements with Events", "https://docs.google.com/document/d/1Q8m5Odwhwdyc64jsPJ6byp7sKSdzEArkRDFmLfrpQ5s/edit?tab=t.0#heading=h.1br8tw1ezfrh"),
            ("Custom Heist Tracks", "https://docs.google.com/document/d/1f6ComClQIJrvrdo5Yu-VmFC7ykKrs_8EyKiMkRRfbhc/edit?tab=t.0#heading=h.wjyyevobb0m0"),
            ("Sticker Replacement", "https://docs.google.com/document/d/15fxhIUzrfkTXYg3EWFLXXid4LNeRUCzecS9SYLJEPwo/edit?usp=sharing"),
            ("Loot Bag Replacement / Body Pillows", "https://docs.google.com/document/d/1PAog1l_E16WBXM8-AJXv2zYaBSpfCAAZ-LvvesOEZ0s/edit?usp=sharing"),
            ("Unique Loot Bags", "https://docs.google.com/document/d/1agtZ2s6NIzRPFCeedPJpXMmlVjrDeO7z1OZNOvKhJl8/edit?usp=sharing"),
            ("Skeletal Mesh Replacement", "https://modworkshop.net/mod/49737")
        ]
        
        # Create and place buttons in a single column
        for name, url in documentation_links:
            ttk.Button(button_frame, text=name, command=lambda u=url: self.open_link(u), style='Green.TButton').pack(pady=5, fill='x')

        # --- Video Tutorial Button Section ---
        # Frame for the video button, placed on the right
        right_frame = ttk.Frame(glass_box, style='TFrame')
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        # This inner frame will vertically center the buttons
        video_button_container = ttk.Frame(right_frame, style='TFrame')
        video_button_container.pack(expand=True)
        
        # Add the "Resources" header
        ttk.Label(video_button_container, text="Resources", font=("Helvetica", 14, "bold"), style='TLabel').pack(pady=(0, 10))

        # Video tutorial button
        video_url = "https://youtube.com/playlist?list=PLRSASA7UrjTvrBML_cbcwKFE6ZnZkRf-C&si=bdRbA17Utq9sP1tC"
        ttk.Button(video_button_container, text="Custom Heist Video Tutorials", 
                   command=lambda: self.open_link(video_url), style='Green.TButton').pack(pady=5, padx=20, fill="x")

        # --- Additional Resources Section ---
        additional_resources = [
            ("Wwise Media IDs", "https://docs.google.com/spreadsheets/d/1Rk0gkPiMuUoGONi914qP1zWtZI421Gsz4QwUvuwGfsk/edit?gid=0#gid=0"),
            ("Wwise Localized Media IDs", "https://docs.google.com/spreadsheets/d/179bC0JiYz54VarSKhQkcYsxAXCnmrTRd_vUWhop_YvM/edit?gid=0#gid=0"),
            ("Gun IDs", "https://docs.google.com/spreadsheets/d/1Me4OK7pksZzkMfCuIqKW-27bGTxro_2q372fwUQYnTY/edit?gid=0#gid=0"),
            ("Female Heister IDs", "https://docs.google.com/spreadsheets/d/16UYUj-X1q94hR0AqaY3PvmlODPEtNKdbOk76D0locmE/edit?usp=sharing"),
            ("Male Heister IDs", "https://docs.google.com/spreadsheets/d/1BwiYpH1KfwB6C6uDalqYCJXt2HOF75H5CQVCEZ_jbuk/edit?usp=sharing"),
            ("PAYDAY 3 Audio Modder","https://modworkshop.net/mod/51045"),
            ("PAYDAY 3 Unreal Locres Editor", "https://modworkshop.net/mod/48158")
            
        ]
        
        # Create and place additional buttons
        for name, url in additional_resources:
            ttk.Button(video_button_container, text=name, 
                       command=lambda u=url: self.open_link(u), style='Green.TButton').pack(pady=5, padx=20, fill="x")


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
