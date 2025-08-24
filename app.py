# app.py
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
import os
import shelve
import logging

# Import the tab classes
from tabs.cleanup import CleanupTab
from tabs.mod_packaging import ModPackagingTab
from tabs.documentation import DocumentationTab
from tabs.credits import CreditsTab

# Import the existing ToolTip class
from utils.tooltip import ToolTip
from utils.styles import apply_styles

# PD3 green accent
GREEN = "#4a663b"

class UEFileDeleterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PAYDAY 3 Modding Tool")
        self.geometry("1024x768")
        self.style = None
        self.root = self

        # Configure logging
        logging.basicConfig(filename=os.path.join("utils", "cleanup.log"), level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

        # Load last folder path from preferences
        self.last_folder_path = ""
        self.load_preferences()

        # Set the window icon
        try:
            icon_path = os.path.join("utils", "icon.png")
            if os.path.exists(icon_path):
                self.icon = PhotoImage(file=icon_path)
                self.iconphoto(False, self.icon)
        except Exception as e:
            logging.error(f"Failed to load window icon: {e}")
        
        # Apply the visual styles
        self.style = ttk.Style(self)
        apply_styles(self.style)

        # Create the main notebook (tabbed interface)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Create and add the tabs
        self.cleanup_tab = CleanupTab(self.notebook, style='TFrame')
        self.mod_packaging_tab = ModPackagingTab(self.notebook, style='TFrame')
        self.documentation_tab = DocumentationTab(self.notebook, style='TFrame')
        self.credits_tab = CreditsTab(self.notebook, style='TFrame')
        
        self.notebook.add(self.cleanup_tab, text="Cleanup")
        self.notebook.add(self.mod_packaging_tab, text="Mod Packaging")
        self.notebook.add(self.documentation_tab, text="Documentation")
        self.notebook.add(self.credits_tab, text="Credits")

        # Create a status bar at the bottom
        self.status_bar = ttk.Label(self, text="Ready", relief='sunken', anchor='w', style='TLabel')
        self.status_bar.pack(side='bottom', fill='x')

        self.check_tabs_for_status_bar()
        
    def check_tabs_for_status_bar(self):
        # Pass the status bar to each tab after they are created
        self.cleanup_tab.status_bar = self.status_bar
        self.mod_packaging_tab.status_bar = self.status_bar
        self.documentation_tab.status_bar = self.status_bar
        self.credits_tab.status_bar = self.status_bar
        
        # Also pass the root window reference if needed (for update_idletasks)
        self.cleanup_tab.root = self
        self.mod_packaging_tab.root = self
        self.documentation_tab.root = self
        self.credits_tab.root = self
        
    def load_preferences(self):
        # Load the last used folder path from the database
        try:
            db_path = os.path.join("utils", "preferences.db")
            with shelve.open(db_path) as db:
                self.last_folder_path = db.get("last_folder_path", "")
        except Exception as e:
            logging.error(f"Failed to load preferences: {e}")
            # Ensure the app can still start if preferences are corrupted
            self.last_folder_path = ""