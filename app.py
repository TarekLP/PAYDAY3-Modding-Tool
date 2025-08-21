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


        self.create_widgets()
        self.check_tabs_for_status_bar()

    def create_widgets(self):
        # Create a style
        self.style = ttk.Style(self)
        apply_styles(self.style)
        
        # Main notebook for tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")
        
        # Create tabs
        self.cleanup_tab = CleanupTab(self.notebook)
        # self.pak_explorer_tab = PakExplorerTab(self.notebook) # Removed this line
        
        # Pass the icon path to the ModPackagingTab
        icon_path = os.path.join("utils", "icon.png")
        self.mod_packaging_tab = ModPackagingTab(self.notebook)
        # Set the icon path as an instance variable on the tab
        self.mod_packaging_tab.default_icon_path = icon_path
        
        self.documentation_tab = DocumentationTab(self.notebook)
        self.credits_tab = CreditsTab(self.notebook)

        # Add tabs to the notebook
        self.notebook.add(self.cleanup_tab, text="Cleanup")
        # self.notebook.add(self.pak_explorer_tab, text="PAK Explorer") # Removed this line
        self.notebook.add(self.mod_packaging_tab, text="Mod Packaging")
        self.notebook.add(self.documentation_tab, text="Documentation")
        self.notebook.add(self.credits_tab, text="Credits")
        
        # Status bar at the bottom
        self.status_bar = ttk.Label(self, text="Ready", relief='sunken', anchor='w', style='TLabel')
        self.status_bar.pack(side='bottom', fill='x')

    def check_tabs_for_status_bar(self):
        # Pass the status bar to each tab after they are created
        self.cleanup_tab.status_bar = self.status_bar
        # if hasattr(self, 'pak_explorer_tab'): # This check is no longer needed
        #     self.pak_explorer_tab.status_bar = self.status_bar
        self.mod_packaging_tab.status_bar = self.status_bar
        self.documentation_tab.status_bar = self.status_bar
        self.credits_tab.status_bar = self.status_bar
        
        # Also pass the root window reference if needed (for update_idletasks)
        self.cleanup_tab.root = self
        # if hasattr(self, 'pak_explorer_tab'): # This check is no longer needed
        #     self.pak_explorer_tab.root = self
        self.mod_packaging_tab.root = self
        self.documentation_tab.root = self
        self.credits_tab.root = self
        
    def load_preferences(self):
        # Load the last used folder path from the database
        try:
            db_path = os.path.join("utils", "preferences.db")
            with shelve.open(db_path) as db:
                if 'last_folder' in db:
                    self.last_folder_path = db['last_folder']
        except Exception as e:
            logging.error(f"Failed to load preferences: {e}")
            self.last_folder_path = ""
