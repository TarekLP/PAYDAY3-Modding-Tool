# tabs/credits.py
import tkinter as tk
from tkinter import ttk
import webbrowser

class CreditsTab(ttk.Frame):
    """
    A tab to display credits and external links.
    """
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.create_widgets()

    def create_widgets(self):
        """
        Creates and lays out the widgets for the credits tab.
        """
        # A framed "glass box" to contain the content with styling
        glass_box = ttk.Frame(self, style='TFrame', padding=(15, 15), relief='groove', borderwidth=2)
        glass_box.pack(expand=True, fill="both", padx=10, pady=10)
        
        # --- App Information Section ---
        ttk.Label(glass_box, text="PD3-Modding-Tool", font=("Helvetica", 16, "bold"), style='TLabel').pack(pady=(5, 5))
        ttk.Label(glass_box, text="A simple tool to help streamline the modding process for Payday 3.", style='TLabel').pack(pady=5)
        
        # --- Author and Libraries Section ---
        ttk.Label(glass_box, text="Author: lenox", font=("Helvetica", 12, "bold"), style='TLabel').pack(pady=(20, 5))
        ttk.Label(glass_box, text="Created with Python and the tkinter library.", style='TLabel').pack()
        
        # --- External Links Section ---
        ttk.Label(glass_box, text="Additional Resources:", font=("Helvetica", 12, "bold"), style='TLabel').pack(pady=(20, 5))

        # Frame for the buttons to keep them side-by-side
        button_frame = ttk.Frame(glass_box, style='TFrame')
        button_frame.pack(pady=10)

        # "Tarek's Carrd Page" button with the new style
        ttk.Button(button_frame, text="Tarek's Carrd Page", command=self.open_tareks_carrd, style='Green.TButton').pack(side='left', padx=5)

        # "Moolah Github" button with the new style
        ttk.Button(button_frame, text="Moolah Github", command=self.open_moolah_github, style='Green.TButton').pack(side='left', padx=5)

    def open_tareks_carrd(self):
        """
        Opens Tarek's Carrd page in the default web browser.
        """
        try:
            webbrowser.open_new("https://greedman.carrd.co/")
        except Exception as e:
            print(f"Failed to open URL: {e}")

    def open_moolah_github(self):
        """
        Opens the Moolah Modding Github page in the default web browser.
        """
        try:
            webbrowser.open_new("https://github.com/MoolahModding")
        except Exception as e:
            print(f"Failed to open URL: {e}")
