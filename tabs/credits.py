# tabs/credits.py
import tkinter as tk
from tkinter import ttk
import webbrowser
from utils.constants import APP_VERSION

class CreditsTab(ttk.Frame):
    """
    A tab to display credits and external links.
    """
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        # We need to make sure status_bar is initialized for this tab.
        self.status_bar = None
        self.create_widgets()

    def create_widgets(self):
        """
        Creates and lays out the widgets for the credits tab.
        """
        # A framed "glass box" to contain the content with styling
        glass_box = ttk.Frame(self, style='TFrame', padding=(15, 15), relief='groove', borderwidth=2)
        glass_box.pack(expand=True, fill="both", padx=10, pady=10)

        # A central frame to hold all content and center it
        content_frame = ttk.Frame(glass_box, style='TFrame')
        content_frame.pack(expand=True)

        # --- App Information Section ---
        ttk.Label(content_frame, text="PAYDAY 3 Modding Tool", font=("Helvetica", 20, "bold"), style='TLabel', anchor='center').pack(pady=(5, 5), fill='x')
        ttk.Label(content_frame, text=APP_VERSION, font=("Helvetica", 10, "italic"), style='TLabel', anchor='center').pack(pady=(0, 10), fill='x')
        ttk.Label(content_frame, text="A simple tool to help streamline the modding process for Payday 3.", style='TLabel', anchor='center', wraplength=500).pack(pady=5, fill='x')

        ttk.Separator(content_frame, orient='horizontal').pack(fill='x', pady=20)

        # --- Acknowledgements Section ---
        ttk.Label(content_frame, text="Acknowledgements", font=("Helvetica", 14, "bold"), style='TLabel', anchor='center').pack(pady=(10, 10), fill='x')
        ttk.Label(content_frame, text="Author: Tarek", style='TLabel', anchor='center').pack(pady=2, fill='x')
        ttk.Label(content_frame, text="Created with Python and the tkinter library.", style='TLabel', anchor='center').pack(pady=2, fill='x')
        thanks_text = "Thanks to Wednesday Enthusiast, ZeroZM0, Cupcake, Ershiozer and Pinki_Ninja for their Contributions to the Documentations."
        ttk.Label(content_frame, text=thanks_text, style='TLabel', anchor='center', wraplength=600).pack(pady=(10, 0), fill='x')

        ttk.Separator(content_frame, orient='horizontal').pack(fill='x', pady=20)

        # --- External Links Section ---
        ttk.Label(content_frame, text="External Links", font=("Helvetica", 14, "bold"), style='TLabel', anchor='center').pack(pady=(10, 10), fill='x')

        # Frame for the buttons to keep them side-by-side
        button_frame = ttk.Frame(content_frame, style='TFrame')
        button_frame.pack(pady=10)

        # "Tarek's Carrd Page" button
        ttk.Button(button_frame, text="Tarek's Carrd Page", command=self.open_tareks_carrd, style='TButton').pack(side='left', padx=5)

        # "Moolah Github" button
        ttk.Button(button_frame, text="Moolah Github", command=self.open_moolah_github, style='TButton').pack(side='left', padx=5)

    def open_tareks_carrd(self):
        """
        Opens Tarek's Carrd page in the default web browser.
        """
        try:
            webbrowser.open_new("https://greedman.carrd.co/")
            if self.status_bar:
                self.status_bar.config(text="Opened Tarek's Carrd page.")
        except Exception as e:
            if self.status_bar:
                self.status_bar.config(text=f"Error opening link: {e}")

    def open_moolah_github(self):
        """
        Opens the Moolah Modding Github page in the default web browser.
        """
        try:
            webbrowser.open_new("https://github.com/MoolahModding")
            if self.status_bar:
                self.status_bar.config(text="Opened Moolah's GitHub page.")
        except Exception as e:
            if self.status_bar:
                self.status_bar.config(text=f"Error opening link: {e}")
