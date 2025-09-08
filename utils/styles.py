# utils/styles.py
import tkinter as tk
from tkinter import ttk

# PD3 green accent
GREEN = "#4a663b"

def apply_styles(style):
    """
    Applies a consistent theme and style configuration to the Tkinter application.
    
    Args:
        style (ttk.Style): The Tkinter Style object.
    """
    style.theme_use('clam')
    style.configure('TFrame', background='#1a1a1a')
    style.configure('TLabel', background='#1a1a1a', foreground='white')
    style.configure('TCheckbutton', background='#1a1a1a', foreground='white', font=('Helvetica', 12))
    
    # Configure a modern dark-themed scrollbar
    style.configure("TScrollbar", troughcolor='#2a2a2a', background='#333333',
                    darkcolor='#333333', lightcolor='#555555', bordercolor='#444444')
    style.map("TScrollbar", background=[('active', '#555555')])

    # Configure the progress bar style and layout
    style.layout('Horizontal.text.Green.TProgressbar', 
                 [('Horizontal.Progressbar.trough', {'sticky': 'nswe'}), 
                  ('Horizontal.Progressbar.pbar', {'sticky': 'nswe'}),
                  ('Horizontal.Progressbar.label', {'sticky': 'nswe'})])
    style.configure('Horizontal.text.Green.TProgressbar', 
                      thickness=10, 
                      troughcolor='#1a1a1a', 
                      background=GREEN, 
                      bordercolor='#1a1a1a', 
                      lightcolor=GREEN, 
                      darkcolor=GREEN,
                      foreground='white',
                      font=('Helvetica', 8, 'bold'))
    
    # Configure the tab styling
    style.configure('TNotebook', background='#1a1a1a', borderwidth=0)
    style.configure('TNotebook.Tab', background='#2a2a2a', foreground='white', padding=[10, 5])
    
    # The green underline is applied by mapping the bordercolor.
    style.map('TNotebook.Tab',
        background=[('selected', '#1a1a1a')],
        foreground=[('selected', 'white')],
        bordercolor=[('selected', GREEN)],
        tabmargins=[('selected', [0, 0, 0, 3])]
    )

    style.configure('TEntry', fieldbackground='#333333', foreground='white', relief='flat')
    
    # Apply consistent styling to all buttons, with larger font and rounded corners
    style.configure('TButton', font=('Helvetica', 12), background=GREEN, foreground='black', relief='flat')
    style.map('TButton', 
        background=[('active', '#668058')],
    )

    # This is the crucial fix for the TclError
    style.layout('TLabelFrame', [('LabelFrame.border', {'sticky': 'nswe'}),
                                 ('LabelFrame.padding', {'sticky': 'nswe', 'children': [
                                     ('LabelFrame.label', {'sticky': 'nw'}),
                                     ('LabelFrame.contents', {'sticky': 'nswe'})
                                 ]})])

    # Configure the LabelFrame title to match the dark theme.
    # While both lines are required, some themes may still show a white background due to rendering quirks.
    style.configure('TLabelFrame', background='#1a1a1a', foreground='white', font=('Helvetica', 12, 'bold'))
    style.configure('TLabelFrame.Label', background='#1a1a1a', foreground='white', font=('Helvetica', 12, 'bold'))
