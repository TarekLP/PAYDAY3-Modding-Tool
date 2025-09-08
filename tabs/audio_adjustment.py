# tabs/audio_adjustment.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import logging
import csv
from utils.tooltip import ToolTip

class AudioAdjustmentTab(ttk.Frame):
    """
    A tab to assist with audio file renaming and organization.
    """
    def __init__(self, parent, last_folder_path="", **kwargs):
        super().__init__(parent, **kwargs)
        self.root = None
        self.status_bar = None
        self.last_folder_path = last_folder_path
        self.file_list = []
        self.id_to_name_map = {}
        self.name_to_id_map = {}

        self.create_widgets()

    def create_widgets(self):
        # A framed "glass box" to contain the content
        glass_box = ttk.Frame(self, style='TFrame', padding=(15, 15), relief='groove', borderwidth=2)
        glass_box.pack(expand=True, fill="both", padx=10, pady=10)

        # Folder selection frame
        folder_frame = ttk.Frame(glass_box, style='TFrame')
        folder_frame.pack(fill='x', pady=5)
        
        ttk.Label(folder_frame, text="Select Work Folder:", style='TLabel').pack(side='left', padx=(0, 0))

        self.folder_path_var = tk.StringVar(value=self.last_folder_path)
        self.folder_path_entry = ttk.Entry(folder_frame, textvariable=self.folder_path_var, width=50, style='TEntry')
        self.folder_path_entry.pack(side='left', expand=True, fill='x', padx=(0, 5))
        
        browse_button = ttk.Button(folder_frame, text="Browse", command=self.browse_folder, style='TButton')
        browse_button.pack(side='left')
        ToolTip(browse_button, "Select the main work folder to find the audio files.")

        # Media CSV selection frame
        media_csv_frame = ttk.Frame(glass_box, style='TFrame')
        media_csv_frame.pack(fill='x', pady=5)
        
        ttk.Label(media_csv_frame, text="Select Media CSV:", style='TLabel').pack(side='left', padx=(0, 0))

        self.media_csv_path_var = tk.StringVar()
        self.media_csv_path_entry = ttk.Entry(media_csv_frame, textvariable=self.media_csv_path_var, width=50, style='TEntry')
        self.media_csv_path_entry.pack(side='left', expand=True, fill='x', padx=(0, 5))
        
        browse_media_csv_button = ttk.Button(media_csv_frame, text="Browse", command=self.browse_media_csv, style='TButton')
        browse_media_csv_button.pack(side='left')
        ToolTip(browse_media_csv_button, "Select the CSV for regular media (SFX, music).")

        # Localized Media CSV selection frame
        localized_csv_frame = ttk.Frame(glass_box, style='TFrame')
        localized_csv_frame.pack(fill='x', pady=5)
        
        ttk.Label(localized_csv_frame, text="Select Localized Media CSV:", style='TLabel').pack(side='left', padx=(0, 0))

        self.localized_csv_path_var = tk.StringVar()
        self.localized_csv_path_entry = ttk.Entry(localized_csv_frame, textvariable=self.localized_csv_path_var, width=50, style='TEntry')
        self.localized_csv_path_entry.pack(side='left', expand=True, fill='x', padx=(0, 5))
        
        browse_localized_csv_button = ttk.Button(localized_csv_frame, text="Browse", command=self.browse_localized_csv, style='TButton')
        browse_localized_csv_button.pack(side='left')
        ToolTip(browse_localized_csv_button, "Select the CSV for localized voice-over files.")

        # Action buttons frame
        action_button_frame = ttk.Frame(glass_box, style='TFrame')
        action_button_frame.pack(pady=10)

        # Rename button
        rename_button = ttk.Button(action_button_frame, text="Rename to Game Files", command=self.start_renaming, style='TButton')
        rename_button.pack(side='left', padx=5)

        # Revert button
        revert_button = ttk.Button(action_button_frame, text="Rename to IDs", command=self.start_reverting, style='TButton')
        revert_button.pack(side='left', padx=5)

        # Progress bar and label
        self.progress_bar = ttk.Progressbar(glass_box, orient='horizontal', length=100, mode='determinate', style='Horizontal.text.Green.TProgressbar')
        self.progress_bar.pack(fill='x', pady=10)
        self.progress_bar_label = ttk.Label(glass_box, text="0%", style='TLabel')
        self.progress_bar_label.pack()

        # Log window section
        log_frame = ttk.LabelFrame(glass_box, text="Log", style='TFrame', padding=(10, 5))
        log_frame.pack(fill='both', expand=True, pady=(5, 0))
        
        self.log_text = tk.Text(log_frame, wrap='word', bg='#1a1a1a', fg='white', relief='flat', state='disabled', font=('Helvetica', 10), insertbackground='white')
        log_scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        self.log_text['yscrollcommand'] = log_scrollbar.set
        
        self.log_text.pack(side='left', fill='both', expand=True)
        log_scrollbar.pack(side='right', fill='y')

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path_var.set(folder_selected)
            if self.root:
                self.root.save_preferences(folder_selected)
            self.update_status(f"Folder selected: {folder_selected}")

    def browse_media_csv(self):
        csv_selected = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv")]
        )
        if csv_selected:
            self.media_csv_path_var.set(csv_selected)
            self.update_status(f"Media CSV selected: {os.path.basename(csv_selected)}")

    def browse_localized_csv(self):
        csv_selected = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv")]
        )
        if csv_selected:
            self.localized_csv_path_var.set(csv_selected)
            self.update_status(f"Localized Media CSV selected: {os.path.basename(csv_selected)}")


    def load_id_map_from_csv(self, file_path):
        id_map = {}
        try:
            with open(file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                # Assuming first row is headers, skip it
                next(reader, None)
                for row in reader:
                    if len(row) >= 2:
                        file_id = row[0].strip()
                        new_name = row[1].strip()
                        if file_id and new_name:
                            id_map[file_id] = new_name
            return id_map
        except Exception as e:
            messagebox.showerror("CSV Error", f"Failed to read CSV file: {e}")
            return None
    
    def load_name_to_id_map_from_csv(self, file_path):
        name_map = {}
        try:
            with open(file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                # Assuming first row is headers, skip it
                next(reader, None)
                for row in reader:
                    if len(row) >= 2:
                        file_id = row[0].strip()
                        new_name = row[1].strip()
                        if file_id and new_name:
                            name_map[new_name] = file_id
            return name_map
        except Exception as e:
            messagebox.showerror("CSV Error", f"Failed to read CSV file: {e}")
            return None
    
    def find_audio_folders(self, root_folder):
        audio_folders = []
        for dirpath, dirnames, filenames in os.walk(root_folder):
            if "wwise" in dirnames:
                wwise_path = os.path.join(dirpath, "wwise")
                for wwise_dir in os.listdir(wwise_path):
                    full_wwise_dir_path = os.path.join(wwise_path, wwise_dir)
                    if os.path.isdir(full_wwise_dir_path):
                        if wwise_dir == "media":
                            audio_folders.append(os.path.join(full_wwise_dir_path, "media"))
                        elif wwise_dir == "localized":
                            localized_path = os.path.join(full_wwise_dir_path, "media")
                            audio_folders.append(localized_path)
        return list(set(audio_folders))


    def start_renaming(self):
        root_folder = self.folder_path_var.get()
        media_csv_path = self.media_csv_path_var.get()
        localized_csv_path = self.localized_csv_path_var.get()

        if not root_folder or not os.path.isdir(root_folder):
            messagebox.showerror("Error", "Please select a valid work folder.")
            return
        
        if not media_csv_path or not os.path.exists(media_csv_path):
            messagebox.showerror("Error", "Please select a valid Media CSV file.")
            return

        if not localized_csv_path or not os.path.exists(localized_csv_path):
            messagebox.showerror("Error", "Please select a valid Localized Media CSV file.")
            return

        media_map = self.load_id_map_from_csv(media_csv_path)
        localized_map = self.load_id_map_from_csv(localized_csv_path)

        if media_map is None or localized_map is None:
            messagebox.showerror("Error", "Failed to load one or both CSV files.")
            return
        
        self.update_status("Finding audio folders...")
        self.log_message("Starting audio file renaming process...")
        
        audio_folders = self.find_audio_folders(root_folder)
        
        if not audio_folders:
            messagebox.showinfo("No Folders Found", "Could not find 'wwise/media' or 'wwise/localized/media' folders.")
            self.update_status("Renaming cancelled. No audio folders found.")
            return

        self.file_list = []
        for folder in audio_folders:
            # Determine which map to use based on the folder path
            if "localized" in os.path.normpath(folder).lower():
                current_map = localized_map
            else:
                current_map = media_map

            for file_name in os.listdir(folder):
                file_id = os.path.splitext(file_name)[0]
                if file_id in current_map:
                    self.file_list.append({
                        "path": os.path.join(folder, file_name),
                        "new_name": current_map[file_id],
                        "id": file_id
                    })

        total_files = len(self.file_list)
        if total_files == 0:
            messagebox.showinfo("No Files", "No files to rename based on the provided dictionaries.")
            self.update_status("Renaming complete. No files were renamed.")
            self.log_message("Renaming complete. No files were found to rename.")
            return

        confirmation = messagebox.askyesno(
            "Confirmation",
            f"Found {total_files} files to rename. Are you sure you want to proceed?"
        )
        if not confirmation:
            self.update_status("Renaming cancelled.")
            self.log_message("Renaming cancelled by user.")
            return

        self.update_status("Renaming files...")
        self.progress_bar["value"] = 0
        self.progress_bar_label.config(text="0%")
        if self.root:
            self.root.update_idletasks()

        for i, file_data in enumerate(self.file_list):
            try:
                # Add the original extension to the new filename
                original_extension = os.path.splitext(file_data["path"])[1]
                new_file_path = os.path.join(os.path.dirname(file_data["path"]), f"{file_data['new_name']}{original_extension}")
                
                os.rename(file_data["path"], new_file_path)
                log_message = f"Renamed {file_data['id']} to {os.path.basename(new_file_path)}"
                self.log_message(log_message)
                logging.info(log_message)
            except Exception as e:
                log_message = f"Failed to rename {file_data['path']}: {e}"
                self.log_message(log_message)
                logging.error(log_message)
            
            progress = (i + 1) / total_files * 100
            self.progress_bar["value"] = progress
            self.progress_bar_label.config(text=f"{progress:.0f}%")
            if self.root:
                self.root.update_idletasks()

        messagebox.showinfo("Renaming Complete", f"Successfully renamed {total_files} files.")
        self.update_status("Renaming complete.")
        self.log_message("Renaming process finished.")
        self.progress_bar["value"] = 100
        self.progress_bar_label.config(text="100%")

    def start_reverting(self):
        root_folder = self.folder_path_var.get()
        media_csv_path = self.media_csv_path_var.get()
        localized_csv_path = self.localized_csv_path_var.get()

        if not root_folder or not os.path.isdir(root_folder):
            messagebox.showerror("Error", "Please select a valid work folder.")
            return
        
        if not media_csv_path or not os.path.exists(media_csv_path):
            messagebox.showerror("Error", "Please select a valid Media CSV file.")
            return

        if not localized_csv_path or not os.path.exists(localized_csv_path):
            messagebox.showerror("Error", "Please select a valid Localized Media CSV file.")
            return
        
        media_map = self.load_name_to_id_map_from_csv(media_csv_path)
        localized_map = self.load_name_to_id_map_from_csv(localized_csv_path)

        if media_map is None or localized_map is None:
            messagebox.showerror("Error", "Failed to load one or both CSV files.")
            return

        self.update_status("Finding audio folders for reversion...")
        self.log_message("Starting audio file reversion process...")

        audio_folders = self.find_audio_folders(root_folder)
        
        if not audio_folders:
            messagebox.showinfo("No Folders Found", "Could not find 'wwise/media' or 'wwise/localized/media' folders.")
            self.update_status("Reversion cancelled. No audio folders found.")
            return

        self.file_list = []
        for folder in audio_folders:
            if "localized" in os.path.normpath(folder).lower():
                current_map = localized_map
            else:
                current_map = media_map

            for file_name in os.listdir(folder):
                file_name_no_ext = os.path.splitext(file_name)[0]
                if file_name_no_ext in current_map:
                    self.file_list.append({
                        "path": os.path.join(folder, file_name),
                        "original_id": current_map[file_name_no_ext],
                        "current_name": file_name_no_ext
                    })

        total_files = len(self.file_list)
        if total_files == 0:
            messagebox.showinfo("No Files", "No files were found to revert based on the provided dictionaries.")
            self.update_status("Reversion complete. No files were reverted.")
            self.log_message("Reversion complete. No files were found to revert.")
            return

        confirmation = messagebox.askyesno(
            "Confirmation",
            f"Found {total_files} files to revert. Are you sure you want to proceed?"
        )
        if not confirmation:
            self.update_status("Reversion cancelled.")
            self.log_message("Reversion cancelled by user.")
            return

        self.update_status("Reverting file names...")
        self.progress_bar["value"] = 0
        self.progress_bar_label.config(text="0%")
        if self.root:
            self.root.update_idletasks()

        for i, file_data in enumerate(self.file_list):
            try:
                original_extension = os.path.splitext(file_data["path"])[1]
                new_file_path = os.path.join(os.path.dirname(file_data["path"]), f"{file_data['original_id']}{original_extension}")
                
                os.rename(file_data["path"], new_file_path)
                log_message = f"Reverted {file_data['current_name']} to {os.path.basename(new_file_path)}"
                self.log_message(log_message)
                logging.info(log_message)
            except Exception as e:
                log_message = f"Failed to revert {file_data['path']}: {e}"
                self.log_message(log_message)
                logging.error(log_message)

            progress = (i + 1) / total_files * 100
            self.progress_bar["value"] = progress
            self.progress_bar_label.config(text=f"{progress:.0f}%")
            if self.root:
                self.root.update_idletasks()

        messagebox.showinfo("Reversion Complete", f"Successfully reverted {total_files} files.")
        self.update_status("Reversion complete.")
        self.log_message("Reversion process finished.")
        self.progress_bar["value"] = 100
        self.progress_bar_label.config(text="100%")
