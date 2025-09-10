# utils/styles.py
import tkinter as tk
import os
from tkinter import ttk

# PD3 green accent
GREEN = "#4a663b"
RED = "#a63232" # For destructive actions


def apply_styles(style):
    """
    Applies a consistent, modern, and sleek theme to the Tkinter application.
    
    Args:
        style (ttk.Style): The Tkinter Style object.
    """
    style.theme_use('clam')

    # --- General Widget Styling ---
    style.configure('.', background='#1a1a1a', foreground='white')
    style.configure('TFrame', background='#1a1a1a') 
    style.configure('TLabel', background='#1a1a1a', foreground='white')
    style.configure('TCheckbutton', background='#1a1a1a', foreground='white', font=('Helvetica', 10))
    style.map('TCheckbutton',
        indicatorcolor=[('selected', GREEN), ('!selected', '#555555')],
        background=[('active', '#2a2a2a')]
    )
    
    # --- Scrollbar ---
    style.configure("TScrollbar", troughcolor='#2a2a2a', background='#444444', bordercolor='#1a1a1a', arrowcolor='white')
    style.map("TScrollbar", background=[('active', '#555555')])

    # --- Progress Bar ---
    style.layout('Horizontal.text.Green.TProgressbar', 
                 [('Horizontal.Progressbar.trough', {'sticky': 'nswe'}), 
                  ('Horizontal.Progressbar.pbar', {'sticky': 'nswe'}),
                  ('Horizontal.Progressbar.label', {'sticky': 'nswe'})])
    style.configure('Horizontal.text.Green.TProgressbar', 
                      thickness=15, 
                      troughcolor='#2a2a2a', 
                      background=GREEN, 
                      bordercolor='#1a1a1a', 
                      lightcolor=GREEN, 
                      darkcolor=GREEN,
                      foreground='white',
                      font=('Helvetica', 8, 'bold'))
    
    # --- Notebook (Tabs) ---
    style.configure('TNotebook', background='#1a1a1a', borderwidth=0)
    # Dim inactive tabs to give focus to the selected one
    style.configure('TNotebook.Tab', background='#2a2a2a', foreground='#bbbbbb', padding=[15, 8], font=('Helvetica', 10, 'bold'))
    
    # Use a top border for the selected tab instead of an underline for a cleaner look
    style.map('TNotebook.Tab',
        background=[('selected', '#1a1a1a')],
        foreground=[('selected', 'white')],
        lightcolor=[('selected', GREEN)],  # This creates a top border in 'clam'
        bordercolor=[('selected', '#1a1a1a')]  # Hide side borders
    )
    # Remove the dotted focus outline on tabs
    style.layout("TNotebook.Tab", [
        ("Notebook.tab", {"sticky": "nswe", "children":
            [("Notebook.padding", {"side": "top", "sticky": "nswe", "children":
                [("Notebook.focus", {"side": "top", "sticky": "nswe", "children":
                    [("Notebook.label", {"side": "top", "sticky": ""})]
                })]
            })]
        })
    ])

    # --- Entry & Combobox Widgets ---
    style.configure('TEntry', fieldbackground='#333333', foreground='white', relief='flat', insertbackground='white', borderwidth=1, bordercolor='#444444')
    style.map('TEntry',
        bordercolor=[('focus', GREEN)],
    )

    # To style the Combobox dropdown list, we need access to the root window's option_database
    try:
        root = style.master
        root.option_add('*TCombobox*Listbox.background', '#333333')
        root.option_add('*TCombobox*Listbox.foreground', 'white')
        root.option_add('*TCombobox*Listbox.selectBackground', GREEN)
        root.option_add('*TCombobox*Listbox.selectForeground', 'white')
        root.option_add('*TCombobox*Listbox.font', ('Helvetica', 10))
        root.option_add('*TCombobox*Listbox.relief', 'flat')
    except Exception:
        # Fails silently if master is not available, though it should be.
        pass

    style.configure('TCombobox',
                    fieldbackground='#333333',
                    foreground='white',
                    relief='flat',
                    arrowsize=15,
                    selectbackground='#333333', # bg of selected item in entry
                    selectforeground='white')
    style.map('TCombobox',
        fieldbackground=[('readonly', '#333333')],
        background=[('readonly', '#333333')]
    )
    
    # --- Button Styling ---
    # Define colors for different button states
    GREEN_ACTIVE = '#567349'
    GREEN_PRESSED = '#405934'
    RED_ACTIVE = '#c24d4d'
    RED_PRESSED = '#8f2b2b'

    # --- Load Button Images from Cache ---
    CACHE_DIR = os.path.join(os.path.dirname(__file__), 'cache')
    os.makedirs(CACHE_DIR, exist_ok=True)
    
    # Load green button images
    style.img_btn_green_normal = tk.PhotoImage(file=os.path.join(CACHE_DIR, "btn_green_normal.png"))
    style.img_btn_green_active = tk.PhotoImage(file=os.path.join(CACHE_DIR, "btn_green_active.png"))
    style.img_btn_green_pressed = tk.PhotoImage(file=os.path.join(CACHE_DIR, "btn_green_pressed.png"))
    
    # Load red button images
    style.img_btn_red_normal = tk.PhotoImage(file=os.path.join(CACHE_DIR, "btn_red_normal.png"))
    style.img_btn_red_active = tk.PhotoImage(file=os.path.join(CACHE_DIR, "btn_red_active.png"))
    style.img_btn_red_pressed = tk.PhotoImage(file=os.path.join(CACHE_DIR, "btn_red_pressed.png"))

    # Create image-based elements. The 'border' option makes them stretchable like 9-patch images.
    style.element_create("Button.background.green", "image", style.img_btn_green_normal,
        ('pressed', style.img_btn_green_pressed),
        ('active', style.img_btn_green_active),
        border=15, sticky="nsew")
    
    style.element_create("Button.background.red", "image", style.img_btn_red_normal,
        ('pressed', style.img_btn_red_pressed),
        ('active', style.img_btn_red_active),
        border=15, sticky="nsew")

    # Redefine the layout for TButton and Red.TButton to use these new image elements
    style.layout("TButton", [("Button.background.green", {"sticky": "nsew", "children": [
        ("TButton.padding", {"sticky": "nsew", "children": [
            ("TButton.label", {"sticky": "nsew"})]})]})])
    
    style.layout("Red.TButton", [("Button.background.red", {"sticky": "nsew", "children": [
        ("TButton.padding", {"sticky": "nsew", "children": [
            ("TButton.label", {"sticky": "nsew"})]})]})])

    # Configure the button styles
    style.configure('TButton', font=('Helvetica', 11, 'bold'), padding=(10, 6), foreground='white', borderwidth=0)
    style.map('TButton', foreground=[('pressed', 'white'), ('active', 'white')], background=[('active', '#1a1a1a')])

    style.configure('Red.TButton', font=('Helvetica', 11, 'bold'), padding=(10, 6), foreground='white', borderwidth=0)
    style.map('Red.TButton', foreground=[('pressed', 'white'), ('active', 'white')], background=[('active', '#1a1a1a')])

    # --- Scale ---
    # This custom style makes the slider thumb a square. A true circle would require an image asset.
    style.configure('Green.Horizontal.TScale',
                    troughcolor='#2a2a2a',
                    background=GREEN,
                    sliderthickness=18, # The height of the slider thumb
                    sliderlength=18)    # The width of the slider thumb
    style.map('Green.Horizontal.TScale',
              background=[('active', '#567349')])

    # The 'sliderlength' option is set in configure. The layout just places the elements.
    # Setting sliderlength equal to sliderthickness makes the thumb a square.
    style.layout('Green.Horizontal.TScale',
                 [('Scale.trough', {'sticky': 'nswe'}),
                  ('Scale.slider', {'side': 'left', 'sticky': ''})])

    # --- LabelFrame ---
    style.layout('TLabelFrame', [('LabelFrame.border', {'sticky': 'nswe'}),
                                 ('LabelFrame.padding', {'sticky': 'nswe', 'children': [
                                     ('LabelFrame.label', {'sticky': 'nw'}),
                                     ('LabelFrame.contents', {'sticky': 'nswe'})
                                 ]})])

    # Configure the LabelFrame to look like a bordered container
    style.configure('TLabelFrame', background='#1a1a1a', borderwidth=1, relief='solid', bordercolor='#444444')
    style.configure('TLabelFrame.Label', background='#1a1a1a', foreground='white', font=('Helvetica', 12, 'bold'))
