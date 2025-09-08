# tabs/cleanup.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import logging
from utils.tooltip import ToolTip
# Import the new styles file
import utils.styles as styles

class CleanupTab(ttk.Frame):
    def __init__(self, parent, last_folder_path="", **kwargs):
        super().__init__(parent, **kwargs)
        self.root = None # Will be set by the main app
        self.status_bar = None # Will be set by the main app
        self.scan_running = False
        self.log_messages = []
        self.last_folder_path = last_folder_path # Store the passed folder path

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
        
        self.create_widgets()

    def create_widgets(self):
        # A framed "glass box" to contain the content
        glass_box = ttk.Frame(self, style='TFrame', padding=(15, 15), relief='groove', borderwidth=2)
        glass_box.pack(expand=True, fill="both", padx=10, pady=10)

        # Folder selection frame
        folder_frame = ttk.Frame(glass_box, style='TFrame')
        folder_frame.pack(fill='x', pady=5)
        
        ttk.Label(folder_frame, text="Select Folder:", style='TLabel').pack(side='left', padx=(0, 5))

        self.folder_path_var = tk.StringVar(value=self.last_folder_path)
        self.folder_path_entry = ttk.Entry(folder_frame, textvariable=self.folder_path_var, width=50, style='TEntry')
        self.folder_path_entry.pack(side='left', expand=True, fill='x', padx=(0, 5))
        
        browse_button = ttk.Button(folder_frame, text="Browse", command=self.browse_folder, style='TButton')
        browse_button.pack(side='left')
        ToolTip(browse_button, "Select the folder containing the mod files you want to clean up.")

        # Scrolled frame for checkboxes
        scrolled_frame = ttk.Frame(glass_box, style='TFrame')
        scrolled_frame.pack(fill='both', expand=True, pady=10)
        
        canvas = tk.Canvas(scrolled_frame, bg='#1a1a1a', highlightthickness=0)
        scrollbar = ttk.Scrollbar(scrolled_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='TFrame')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Grid for the categories inside the scrollable frame
        scrollable_frame.grid_columnconfigure(0, weight=1)
        
        for category_index, (category, prefixes) in enumerate(self.prefixes_by_category.items()):
            # Create a checkbutton for the whole category
            category_var = tk.BooleanVar(value=True)
            self.prefix_vars[category] = category_var
            category_cb = ttk.Checkbutton(scrollable_frame, text=category, variable=category_var, style='TCheckbutton')
            category_cb.grid(row=category_index*2, column=0, sticky='w', padx=(10,0))
            category_cb.configure(command=lambda cv=category_var, pfxs=prefixes: self.select_category(cv.get(), pfxs))
            
            # Create a frame to hold the individual prefix checkboxes
            prefix_frame = ttk.Frame(scrollable_frame, style='TFrame')
            prefix_frame.grid(row=category_index*2, column=1, sticky='w', padx=(0, 10))
            
            # Create individual checkbuttons for each prefix
            for prefix_index, prefix in enumerate(prefixes):
                prefix_var = tk.BooleanVar(value=True)
                self.prefix_vars[prefix] = prefix_var
                prefix_cb = ttk.Checkbutton(prefix_frame, text=prefix, variable=prefix_var, style='TCheckbutton')
                prefix_cb.grid(row=prefix_index, column=0, sticky='w', padx=5, pady=2)

            # Add separator between categories, but not after the last one
            if category_index < len(self.prefixes_by_category) - 1:
                separator_label = ttk.Label(scrollable_frame, text="---------------------------------", style='TLabel')
                separator_label.grid(row=category_index*2 + 1, column=0, columnspan=2, sticky='ew', pady=5)
                
        # Action buttons frame
        action_frame = ttk.Frame(glass_box, style='TFrame')
        action_frame.pack(fill='x', pady=10)

        # Scan and Delete buttons
        ttk.Button(action_frame, text="Scan Files", command=self.scan_files, style='TButton').pack(side='left', padx=(0, 5))
        ttk.Button(action_frame, text="Delete Files", command=self.delete_files, style='Red.TButton').pack(side='left', padx=(5, 0))

        # Progress bar and label
        self.progress_bar = ttk.Progressbar(glass_box, orient='horizontal', length=100, mode='determinate', style='Horizontal.text.Green.TProgressbar')
        self.progress_bar.pack(fill='x', pady=10)
        self.progress_bar_label = ttk.Label(glass_box, text="0%", style='TLabel')
        self.progress_bar_label.pack()

        # Log window section
        log_frame = ttk.LabelFrame(glass_box, text="Log", style='TFrame', padding=(10, 5))
        log_frame.pack(fill='both', expand=True, pady=(5, 0))
        
        self.log_text = tk.Text(log_frame, wrap='word', bg='#2a2a2a', fg='white', relief='flat', state='disabled', font=('Helvetica', 10), insertbackground='white')
        log_scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        self.log_text['yscrollcommand'] = log_scrollbar.set
        
        self.log_text.pack(side='left', fill='both', expand=True)
        log_scrollbar.pack(side='right', fill='y')


    def select_category(self, checked, prefixes):
        # Select/deselect all individual checkboxes in a category
        for prefix in prefixes:
            if prefix in self.prefix_vars:
                self.prefix_vars[prefix].set(checked)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path_var.set(folder_selected)
            if self.root:
                self.root.save_preferences(folder_selected)
            self.update_status(f"Folder selected: {folder_selected}")

    def scan_files(self):
        folder_path = self.folder_path_var.get()
        if not folder_path or not os.path.isdir(folder_path):
            messagebox.showerror("Error", "Please select a valid folder.")
            return

        self.update_status("Scanning files...")
        self.log_message("Starting scan...")

        selected_prefixes = []
        for category, prefixes in self.prefixes_by_category.items():
            if self.prefix_vars.get(category) and self.prefix_vars[category].get():
                selected_prefixes.extend(prefixes)
            else:
                for prefix in prefixes:
                    if self.prefix_vars.get(prefix) and self.prefix_vars[prefix].get():
                        selected_prefixes.append(prefix)
        
        files_to_delete = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                for prefix in selected_prefixes:
                    if file.startswith(prefix) and (file.endswith(".uasset") or file.endswith(".umap")):
                        files_to_delete.append(os.path.join(root, file))
                        self.log_message(f"Found: {os.path.join(root, file)}")
                        break

        num_files = len(files_to_delete)
        messagebox.showinfo("Scan Complete", f"Found {num_files} files to delete.")
        self.update_status(f"Scan complete. Found {num_files} files.")
        self.log_message(f"Scan complete. Found {num_files} files to delete.")
        
        self.log_messages = files_to_delete

    def delete_files(self):
        files_to_delete = self.log_messages
        total_files = len(files_to_delete)

        if total_files == 0:
            messagebox.showinfo("No Files", "No files to delete.")
            self.update_status("No files to delete.")
            self.log_message("No files to delete.")
            return
        
        confirmation = messagebox.askyesno(
            "Confirmation",
            f"Are you sure you want to delete {total_files} files? This action cannot be undone."
        )
        if not confirmation:
            self.update_status("Deletion cancelled.")
            self.log_message("Deletion cancelled.")
            return

        self.update_status("Deleting files...")
        self.log_message("Starting deletion...")
        self.progress_bar["value"] = 0
        self.progress_bar_label.config(text="0%")
        if self.root:
            self.root.update_idletasks()

        # Deletion logic with progress bar
        if total_files > 0:
            for i, file_path in enumerate(files_to_delete):
                try:
                    os.remove(file_path)
                    log_message = f"Successfully deleted: {file_path}"
                    self.log_message(log_message)
                    logging.info(log_message)
                except Exception as e:
                    log_message = f"Failed to delete {file_path}: {e}"
                    self.log_message(log_message)
                    logging.error(log_message)
                
                # Update progress bar
                progress = (i + 1) / total_files * 100
                self.progress_bar["value"] = progress
                self.progress_bar_label.config(text=f"{progress:.0f}%")
                if self.root:
                    self.root.update_idletasks()

            messagebox.showinfo("Deletion Complete", f"Deleted {total_files} files.")
        
        self.update_status("Deletion complete.")
        self.log_message("Deletion process finished.")
        self.progress_bar["value"] = 100
        self.progress_bar_label.config(text="100%")

    def update_status(self, message):
        if self.status_bar:
            self.status_bar.config(text=message)

    def log_message(self, message):
        self.log_text.configure(state='normal')
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state='disabled')
