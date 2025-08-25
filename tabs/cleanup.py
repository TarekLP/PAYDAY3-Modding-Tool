# tabs/cleanup.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import logging
from utils.tooltip import ToolTip
# Import the new styles file
import utils.styles as styles

class CleanupTab(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.root = None # Will be set by the main app
        self.status_bar = None # Will be set by the main app
        self.scan_running = False
        self.log_messages = []

        # Dictionary to store Checkbutton variables for easy access.
        # All prefixes now end with an underscore for consistency.
        self.prefix_vars = {}
        self.prefixes_by_category = {
            "Audio Prefixes": ["LPS_", "WAV_", "MP3_", "OGG_", "SND_", "AUD_"],
            "Textures Prefixes": ["T_", "TD_", "N_", "R_"],
            "Materials Prefixes": ["M_", "MI_", "ML_", "MLB_", "MM_", "MF_", "MAT_"],
            "Blueprint Prefixes": ["BP_", "PC_", "WBP_", "BT_"],
            "Animation Prefixes": ["A_", "ABP_", "AM_", "AO_", "BS_", "SK_", "SKM_", "PA_", "ABM_", "ANIM_", "ANM_"],
            "Mesh Prefixes": ["SM_", "SK_", "PM_", "UM_", "STAT_", "INST_"],
            "Niagara Prefixes": ["N_", "NS_"],
            "UI Prefixes": ["WBP_", "UI_"],
            "VFX Prefixes": ["FX_", "VFX_"],
            "Misc Prefixes": ["_C", "SBZ_", "BB_", "C_", "CT_", "DA_", "EQS_", "FFE_", "FT_", "SS_", "ST_", "SLOT_", "Var_", "WAD_", "WGD_", "WMD_", "WPD_", "WSD_", "WTD_"]
        }
        
        # Merge all prefixes into a single list for the Checkbutton frame
        self.all_prefixes = sorted(list(set([p for sublist in self.prefixes_by_category.values() for p in sublist])))
        
        # Correctly call apply_styles by passing a ttk.Style object
        styles.apply_styles(ttk.Style(parent))

        self.create_widgets()

    def create_widgets(self):
        # Frame for folder selection and buttons
        top_frame = ttk.Frame(self)
        top_frame.pack(fill='x', padx=10, pady=10)

        # Folder selection label and entry
        folder_label = ttk.Label(top_frame, text="Target Folder:")
        folder_label.pack(side='left', padx=(0, 5))

        self.folder_entry = ttk.Entry(top_frame, width=50)
        self.folder_entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
        if self.root and self.root.last_folder_path:
            self.folder_entry.insert(0, self.root.last_folder_path)

        # Browse button
        browse_button = ttk.Button(top_frame, text="Browse", command=self.browse_folder)
        browse_button.pack(side='left')
        
        # Frame for the list of prefixes, now with a centered layout
        list_container_frame = ttk.Frame(self)
        list_container_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))

        # Main frame for the scrollable list, centered within its container
        list_frame = ttk.Frame(list_container_frame)
        list_frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.95, relheight=0.95)

        # Create a canvas and scrollbar for the prefixes list
        self.canvas = tk.Canvas(list_frame, background='#1a1a1a', highlightthickness=0)
        self.canvas.pack(side='left', fill='both', expand=True)
        
        # Configure the scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame inside the canvas to hold the checkbuttons
        self.checkbutton_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.checkbutton_frame, anchor="nw")

        self.canvas.bind('<Configure>', self.on_frame_configure)
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        # Populate the scrollable list with prefixes and categories
        for category, prefixes in self.prefixes_by_category.items():
            # Create a bold label for the category
            category_label = ttk.Label(self.checkbutton_frame, text=category, font=('Helvetica', 12, 'bold'))
            category_label.pack(anchor='w', padx=5, pady=(10, 0))
            # Bind the label to a function that selects all prefixes in the category
            category_label.bind("<Button-1>", lambda event, cat=category: self.select_category(cat))

            # Create Checkbuttons for each prefix in the category
            for prefix in prefixes:
                var = tk.BooleanVar(value=False)
                cb = ttk.Checkbutton(self.checkbutton_frame, text=prefix, variable=var, onvalue=True, offvalue=False)
                cb.pack(anchor='w', padx=20)
                self.prefix_vars[prefix] = var
                # Set up a tooltip for each checkbox
                ToolTip(cb, text=f"Select all files with the prefix '{prefix}'")
        
        # Frame for the action buttons at the bottom
        bottom_frame = ttk.Frame(self)
        bottom_frame.pack(fill='x', padx=10, pady=(0, 10))

        # Progress bar
        self.progress_bar = ttk.Progressbar(bottom_frame, style='Horizontal.text.Green.TProgressbar', orient='horizontal', length=100, mode='determinate')
        self.progress_bar.pack(fill='x', expand=True, pady=(0, 5))
        self.progress_bar_label = ttk.Label(self.progress_bar, text="0%", style='TLabel')
        self.progress_bar_label.place(relx=0.5, rely=0.5, anchor='center')

        # Action buttons
        delete_button = ttk.Button(bottom_frame, text="Delete Selected", command=self.delete_files)
        delete_button.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        log_button = ttk.Button(bottom_frame, text="Show Log", command=self.show_log_output)
        log_button.pack(side='right', fill='x', expand=True, padx=(5, 0))

    def on_frame_configure(self, event):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mousewheel(self, event):
        """Allows mousewheel scrolling on the canvas"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def select_category(self, category):
        """Selects all checkbuttons in a given category."""
        prefixes = self.prefixes_by_category.get(category, [])
        is_all_selected = all(self.prefix_vars[p].get() for p in prefixes if p in self.prefix_vars)
        
        for prefix in prefixes:
            if prefix in self.prefix_vars:
                # Toggle selection based on if all are currently selected
                self.prefix_vars[prefix].set(not is_all_selected)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory(initialdir=self.root.last_folder_path)
        if folder_selected:
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder_selected)
            self.root.last_folder_path = folder_selected
            self.status_bar.config(text=f"Folder selected: {folder_selected}")

    def scan_for_files(self, folder_path, selected_prefixes):
        """Scans the specified folder for files with selected prefixes and returns a list of them."""
        files_to_delete = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                if any(file.startswith(prefix) for prefix in selected_prefixes):
                    files_to_delete.append(os.path.join(root, file))
        return files_to_delete

    def show_log_output(self):
        """Displays the log of the last deletion process in a new window."""
        log_window = tk.Toplevel(self.root)
        log_window.title("Deletion Log")
        log_window.geometry("600x400")
        log_window.configure(bg='#1a1a1a')
        
        # Use a Text widget for the log output to handle large amounts of text
        log_text = tk.Text(log_window, wrap='word', bg='#1a1a1a', fg='white', relief='flat', font=('Helvetica', 10))
        log_text.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Add a scrollbar to the Text widget
        scrollbar = ttk.Scrollbar(log_window, command=log_text.yview)
        log_text['yscrollcommand'] = scrollbar.set
        scrollbar.pack(side='right', fill='y')

        if not self.log_messages:
            log_text.insert(tk.END, "No logs available. Run a deletion process first.")
        else:
            log_text.insert(tk.END, "\n".join(self.log_messages))
            log_text.yview_moveto('1.0') # Scroll to the top

    def delete_files(self):
        folder_path = self.folder_entry.get()
        if not folder_path or not os.path.exists(folder_path):
            messagebox.showerror("Error", "Please select a valid folder.")
            return

        selected_prefixes = [p for p, var in self.prefix_vars.items() if var.get()]
        if not selected_prefixes:
            messagebox.showinfo("Info", "No prefixes selected for deletion.")
            return
        
        # Clear previous logs
        self.log_messages = []

        # Scan for files before asking for confirmation
        files_to_delete = self.scan_for_files(folder_path, selected_prefixes)
        
        total_files = len(files_to_delete)
        if total_files == 0:
            messagebox.showinfo("Deletion Complete", "No matching files found to delete.")
            return
            
        confirmation = messagebox.askyesno("Confirm Deletion", 
                                           f"Found {total_files} files to delete. Are you sure you want to delete them in:\n{folder_path}?\nThis action cannot be undone.")
        if not confirmation:
            self.status_bar.config(text="Deletion cancelled.")
            return

        self.status_bar.config(text="Deleting files...")
        self.progress_bar["value"] = 0
        self.progress_bar_label.config(text="0%")
        self.root.update_idletasks()

        # Deletion logic with progress bar
        if total_files > 0:
            for i, file_path in enumerate(files_to_delete):
                try:
                    os.remove(file_path)
                    log_message = f"Successfully deleted: {file_path}"
                    self.log_messages.append(log_message)
                    logging.info(log_message)
                except Exception as e:
                    log_message = f"Failed to delete {file_path}: {e}"
                    self.log_messages.append(log_message)
                    logging.error(log_message)
                
                # Update progress bar
                progress = (i + 1) / total_files * 100
                self.progress_bar["value"] = progress
                self.progress_bar_label.config(text=f"{progress:.0f}%")
                self.root.update_idletasks()

            messagebox.showinfo("Deletion Complete", f"Deleted {total_files} files.")
        
        self.status_bar.config(text="Deletion complete.")
        self.progress_bar["value"] = 100
        self.progress_bar_label.config(text="100%")
        self.root.update_idletasks()
