# app.py
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
import os
import shelve
import logging
from tkinterdnd2 import TkinterDnD

# Import the tab classes
from tabs.cleanup import CleanupTab
from tabs.mod_packaging import ModPackagingTab
from tabs.documentation import DocumentationTab
from tabs.credits import CreditsTab
# Import the AudioAdjustmentTab class
from tabs.audio_adjustment import AudioAdjustmentTab
from tabs.music_tab import MusicTab

# Import the existing ToolTip class
from utils.tooltip import ToolTip
from utils.styles import apply_styles

# PD3 green accent
GREEN = "#4a663b"

class UEFileDeleterApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("PAYDAY 3 Modding Tool")
        self.geometry("1280x720")
        self.style = None
        self.root = self

        # Configure logging
        logging.basicConfig(filename=os.path.join("utils", "cleanup.log"), level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

        # Load last folder path from preferences
        self.last_folder_path = ""
        self.last_media_csv_path = ""
        self.last_localized_csv_path = ""
        self.load_preferences()

        # Set the window icon
        try:
            icon_path = os.path.join("utils", "icon.png")
            if os.path.exists(icon_path):
                self.icon = PhotoImage(file=icon_path)
                self.iconphoto(False, self.icon)
        except Exception as e:
            logging.error(f"Failed to load icon: {e}")

        # Apply custom styles
        self.style = ttk.Style(self)
        apply_styles(self.style)

        # Create the notebook (tabbed interface)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')

        # Create the tabs and add them to the notebook
        self.cleanup_tab = CleanupTab(self.notebook, last_folder_path=self.last_folder_path)
        self.mod_packaging_tab = ModPackagingTab(self.notebook)
        # Pass the saved CSV paths to the audio adjustment tab
        self.audio_adjustment_tab = AudioAdjustmentTab(self.notebook,
                                                       last_folder_path=self.last_folder_path,
                                                       last_media_csv_path=self.last_media_csv_path,
                                                       last_localized_csv_path=self.last_localized_csv_path)
        self.documentation_tab = DocumentationTab(self.notebook)
        self.credits_tab = CreditsTab(self.notebook)
        
        self.music_tab = MusicTab(self.notebook, root=self, music_volume=self.music_volume)

        self.notebook.add(self.cleanup_tab, text="Cleanup")
        self.notebook.add(self.audio_adjustment_tab, text="Audio Adjustment")
        self.notebook.add(self.mod_packaging_tab, text="Mod Packaging")
        self.notebook.add(self.documentation_tab, text="Documentation")
        self.notebook.add(self.credits_tab, text="Credits")
        self.notebook.add(self.music_tab, text="Music Player")

        # Create a status bar at the bottom
        self.status_bar = ttk.Label(self, text="Ready", relief='sunken', anchor='w', style='TLabel')
        self.status_bar.pack(side='bottom', fill='x')

        self.check_tabs_for_status_bar()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def check_tabs_for_status_bar(self):
        # Pass the status bar to each tab after they are created
        self.cleanup_tab.status_bar = self.status_bar
        self.mod_packaging_tab.status_bar = self.status_bar
        self.audio_adjustment_tab.status_bar = self.status_bar
        self.documentation_tab.status_bar = self.status_bar
        self.credits_tab.status_bar = self.status_bar
        self.music_tab.status_bar = self.status_bar
        
        # Also pass the root window reference if needed (for update_idletasks)
        self.cleanup_tab.root = self
        self.mod_packaging_tab.root = self
        self.audio_adjustment_tab.root = self
        self.documentation_tab.root = self
        self.credits_tab.root = self
        self.music_tab.root = self
        
    def load_preferences(self):
        # Load the last used folder path and CSV paths from the database
        try:
            db_path = os.path.join("utils", "preferences.db")
            with shelve.open(db_path) as db:
                self.last_folder_path = db.get("last_folder_path", "")
                self.last_media_csv_path = db.get("last_media_csv_path", "")
                self.last_localized_csv_path = db.get("last_localized_csv_path", "")
                # Load music preferences
                self.music_volume = db.get("music_volume", 0.5)
                self.music_is_playing = db.get("music_is_playing", False)
        except Exception as e:
            logging.error(f"Failed to load preferences: {e}")

    def save_preferences(self, folder_path=None, media_csv_path=None, localized_csv_path=None, music_volume=None, music_is_playing=None):
        # Save the last used folder path and CSV paths to the database
        try:
            db_path = os.path.join("utils", "preferences.db")
            with shelve.open(db_path) as db:
                if folder_path is not None:
                    db["last_folder_path"] = folder_path
                if media_csv_path is not None:
                    db["last_media_csv_path"] = media_csv_path
                if localized_csv_path is not None:
                    db["last_localized_csv_path"] = localized_csv_path
                if music_volume is not None:
                    db["music_volume"] = music_volume
                if music_is_playing is not None:
                    db["music_is_playing"] = music_is_playing
        except Exception as e:
            logging.error(f"Failed to save preferences: {e}")

    def on_closing(self):
        """Called when the user closes the window."""
        self.destroy()
