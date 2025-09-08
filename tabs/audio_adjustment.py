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
    def __init__(self, parent, last_folder_path="", last_media_csv_path="", last_localized_csv_path="", **kwargs):
        super().__init__(parent, **kwargs)
        self.root = None
        self.status_bar = None
        self.last_folder_path = last_folder_path
        self.last_media_csv_path = last_media_csv_path
        self.last_localized_csv_path = last_localized_csv_path
        self.file_list = []
        self.id_to_name_map = {}
        self.name_to_id_map = {}
        
        # New variable for the dropdown selection
        self.file_type_var = tk.StringVar(value="All")

        self.create_widgets()

    def create_widgets(self):
        # A framed "glass box" to contain the content
        glass_box = ttk.Frame(self, style='TFrame', padding=(15, 15), relief='groove', borderwidth=2)
        glass_box.pack(expand=True, fill="both", padx=10, pady=10)

        # --- Configuration Section ---
        config_frame = ttk.Frame(glass_box, style='TFrame', padding=(10, 10), relief='groove', borderwidth=1)
        config_frame.pack(fill='x', pady=(0, 10))
        
        config_title = ttk.Label(config_frame, text="Configuration", style='TLabel', font=("Helvetica", 12, "bold"))
        config_title.pack(anchor='w', pady=(0, 10))

        # Folder selection frame
        folder_frame = ttk.Frame(config_frame, style='TFrame')
        folder_frame.pack(fill='x', pady=5)
        
        ttk.Label(folder_frame, text="Select Work Folder:", style='TLabel', width=28).pack(side='left', padx=(0, 5))

        self.folder_path_var = tk.StringVar(value=self.last_folder_path)
        self.folder_path_entry = ttk.Entry(folder_frame, textvariable=self.folder_path_var, style='TEntry')
        self.folder_path_entry.pack(side='left', expand=True, fill='x', padx=(0, 5))
        
        browse_button = ttk.Button(folder_frame, text="Browse", command=self.browse_folder, style='TButton')
        browse_button.pack(side='left')
        ToolTip(browse_button, "Select the main work folder to find the audio files.")
        
        # Dropdown for selecting file type to process
        options_frame = ttk.Frame(config_frame, style='TFrame')
        options_frame.pack(fill='x', pady=5)
        
        ttk.Label(options_frame, text="Select File Type to Process:", style='TLabel', width=28).pack(side='left', padx=(0, 5))
        
        self.file_type_combobox = ttk.Combobox(options_frame, textvariable=self.file_type_var, state='readonly', style='TCombobox')
        self.file_type_combobox['values'] = ("All", "Media (Audio)", "Localized (VO)")
        self.file_type_combobox.pack(side='left', expand=False, padx=(0, 10))
        self.file_type_combobox.set("All")

        # Media CSV selection frame
        media_csv_frame = ttk.Frame(config_frame, style='TFrame')
        media_csv_frame.pack(fill='x', pady=5)
        
        ttk.Label(media_csv_frame, text="Select Media CSV:", style='TLabel', width=28).pack(side='left', padx=(0, 5))

        self.media_csv_path_var = tk.StringVar(value=self.last_media_csv_path)
        self.media_csv_path_entry = ttk.Entry(media_csv_frame, textvariable=self.media_csv_path_var, style='TEntry')
        self.media_csv_path_entry.pack(side='left', expand=True, fill='x', padx=(0, 5))
        
        browse_media_csv_button = ttk.Button(media_csv_frame, text="Browse", command=self.browse_media_csv, style='TButton')
        browse_media_csv_button.pack(side='left')
        ToolTip(browse_media_csv_button, "Select the CSV for regular media (SFX, music).")

        # Localized Media CSV selection frame
        localized_csv_frame = ttk.Frame(config_frame, style='TFrame')
        localized_csv_frame.pack(fill='x', pady=5)
        
        ttk.Label(localized_csv_frame, text="Select Localized Media CSV:", style='TLabel', width=28).pack(side='left', padx=(0, 5))

        self.localized_csv_path_var = tk.StringVar(value=self.last_localized_csv_path)
        self.localized_csv_path_entry = ttk.Entry(localized_csv_frame, textvariable=self.localized_csv_path_var, style='TEntry')
        self.localized_csv_path_entry.pack(side='left', expand=True, fill='x', padx=(0, 5))
        
        browse_localized_csv_button = ttk.Button(localized_csv_frame, text="Browse", command=self.browse_localized_csv, style='TButton')
        browse_localized_csv_button.pack(side='left')
        ToolTip(browse_localized_csv_button, "Select the CSV for localized voice-over files.")

        # --- Actions & Progress Section ---
        action_progress_frame = ttk.Frame(glass_box, style='TFrame', padding=(10, 10), relief='groove', borderwidth=1)
        action_progress_frame.pack(fill='x', pady=10)

        action_title = ttk.Label(action_progress_frame, text="Actions & Progress", style='TLabel', font=("Helvetica", 12, "bold"))
        action_title.pack(anchor='w', pady=(0, 10))

        # Action buttons frame
        action_button_frame = ttk.Frame(action_progress_frame, style='TFrame')
        action_button_frame.pack(pady=5)

        # Rename button
        rename_button = ttk.Button(action_button_frame, text="Rename to Game Files", command=self.start_renaming, style='TButton')
        rename_button.pack(side='left', padx=5)

        # Revert button
        revert_button = ttk.Button(action_button_frame, text="Rename to IDs", command=self.start_reverting, style='TButton')
        revert_button.pack(side='left', padx=5)

        # Progress bar and label
        self.progress_bar = ttk.Progressbar(action_progress_frame, orient='horizontal', length=100, mode='determinate', style='Horizontal.text.Green.TProgressbar')
        self.progress_bar.pack(fill='x', pady=(10, 5))
        self.progress_bar_label = ttk.Label(action_progress_frame, text="0%", style='TLabel', anchor='center')
        self.progress_bar_label.pack(fill='x')

        # --- Log Section ---
        log_frame = ttk.Frame(glass_box, style='TFrame', padding=(10, 5), relief='groove', borderwidth=1)
        log_frame.pack(fill='both', expand=True, pady=(5, 0))
        
        log_title = ttk.Label(log_frame, text="Log", style='TLabel', font=("Helvetica", 12, "bold"))
        log_title.pack(anchor='w', pady=(0, 5))

        self.log_text = tk.Text(log_frame, wrap='word', bg='#2a2a2a', fg='white', relief='flat', state='disabled', font=('Helvetica', 10), insertbackground='white')
        log_scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        self.log_text['yscrollcommand'] = log_scrollbar.set
        
        self.log_text.pack(side='left', fill='both', expand=True)
        log_scrollbar.pack(side='right', fill='y')

    def update_status(self, message):
        """Updates the text of the main application's status bar."""
        if self.status_bar:
            self.status_bar.config(text=message)

    def log_message(self, message):
        """Appends a message to the log text widget."""
        self.log_text.configure(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state='disabled')

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path_var.set(folder_selected)
            if self.root:
                self.root.save_preferences(folder_path=folder_selected)
            self.update_status(f"Folder selected: {folder_selected}")

    def browse_media_csv(self):
        csv_selected = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv")]
        )
        if csv_selected:
            self.media_csv_path_var.set(csv_selected)
            if self.root:
                self.root.save_preferences(media_csv_path=csv_selected)
            self.update_status(f"Media CSV selected: {os.path.basename(csv_selected)}")

    def browse_localized_csv(self):
        csv_selected = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv")]
        )
        if csv_selected:
            self.localized_csv_path_var.set(csv_selected)
            if self.root:
                self.root.save_preferences(localized_csv_path=csv_selected)
            self.update_status(f"Localized Media CSV selected: {os.path.basename(csv_selected)}")

    def load_id_map_from_csv(self, file_path):
        """Loads a map from Wwise ID to Name, assuming CSV format 'Name,Wwise Id'."""
        id_map = {}
        id_map_lower = {}
        try:
            with open(file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                # Skip the first 7 rows as they are headers based on user feedback
                for _ in range(7):
                    next(reader, None)
                for row in reader:
                    if len(row) >= 2:
                        new_name = row[0].strip()
                        file_id = row[1].strip()
                        if file_id and new_name:
                            id_map[file_id] = new_name
                            id_map_lower[file_id.lower()] = new_name
            return id_map, id_map_lower
        except Exception as e:
            messagebox.showerror("CSV Error", f"Failed to read CSV file: {e}")
            return None, None
    
    def load_name_to_id_map_from_csv(self, file_path):
        """Loads a map from Name to Wwise ID, assuming CSV format 'Name,Wwise Id'."""
        name_map = {}
        name_map_lower = {}
        try:
            with open(file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                # Skip the first 7 rows as they are headers
                for _ in range(7):
                    next(reader, None)
                for row in reader:
                    if len(row) >= 2:
                        file_id = row[1].strip()
                        new_name = row[0].strip()
                        if file_id and new_name:
                            if new_name.lower() in name_map_lower:
                                self.log_message(f"Warning: Found a duplicate name '{new_name}'. Skipping to prevent ambiguous reversion.")
                                logging.warning(f"Found duplicate name '{new_name}' in CSV. Reversion for this file may not be possible.")
                                # We do not add the duplicate to the map to avoid ambiguity
                                continue
                            name_map[new_name] = file_id
                            name_map_lower[new_name.lower()] = file_id
            return name_map, name_map_lower
        except Exception as e:
            messagebox.showerror("CSV Error", f"Failed to read CSV file: {e}")
            return None, None
    
    def find_audio_folders(self, root_folder):
        """
        Finds the 'Media' and 'Localized/English_US_/Media' subdirectories
        within the given root folder.
        """
        audio_folders = []
        
        # Check for the main Media folder
        media_path = os.path.join(root_folder, "Content", "WwiseAudio", "Media")
        if os.path.isdir(media_path):
            audio_folders.append(media_path)
        
        # Check for the Localized/Media folder
        localized_media_path = os.path.join(root_folder, "Content", "WwiseAudio", "Localized", "English_US_", "Media")
        if os.path.isdir(localized_media_path):
            audio_folders.append(localized_media_path)

        return audio_folders


    def start_renaming(self):
        root_folder = self.folder_path_var.get()
        media_csv_path = self.media_csv_path_var.get()
        localized_csv_path = self.localized_csv_path_var.get()
        selected_type = self.file_type_var.get()
        
        # The list of file extensions to process
        allowed_extensions = ['.uasset', '.uexp', '.ubulk', '.wav']

        if not root_folder or not os.path.isdir(root_folder):
            messagebox.showerror("Error", "Please select a valid work folder.")
            return
        
        if not media_csv_path and not localized_csv_path:
            messagebox.showerror("Error", "Please select at least one CSV file to proceed.")
            return

        media_map_lower = {}
        localized_map_lower = {}

        if media_csv_path and os.path.exists(media_csv_path):
            _, media_map_lower = self.load_id_map_from_csv(media_csv_path)
            if media_map_lower is None: return # Stop if loading failed
        
        if localized_csv_path and os.path.exists(localized_csv_path):
            _, localized_map_lower = self.load_id_map_from_csv(localized_csv_path)
            if localized_map_lower is None: return # Stop if loading failed
        
        self.update_status("Finding audio folders...")
        self.log_message("Starting audio file renaming process...")
        
        audio_folders = self.find_audio_folders(root_folder)
        
        if not audio_folders:
            messagebox.showinfo("No Folders Found", "Could not find 'Media' or 'Localized/English_US_/Media' folders within the selected directory. Please ensure you have selected the main 'PAYDAY3' folder.")
            self.update_status("Renaming cancelled. No audio folders found.")
            return

        self.file_list = []
        for folder in audio_folders:
            is_localized_folder = "Localized" in os.path.normpath(folder)

            current_map_lower = None
            if selected_type == "All":
                current_map_lower = localized_map_lower if is_localized_folder else media_map_lower
            elif selected_type == "Localized (VO)" and is_localized_folder:
                current_map_lower = localized_map_lower
            elif selected_type == "Media (Audio)" and not is_localized_folder:
                current_map_lower = media_map_lower
            
            if current_map_lower:
                for file_name in os.listdir(folder):
                    file_id_raw, extension = os.path.splitext(file_name)
                    # Strip any leading/trailing whitespace from the file ID
                    file_id = file_id_raw.strip()
                    # Check if the file's ID is in the dictionary from the CSV
                    if file_id.lower() in current_map_lower:
                        # Now, check if the file's extension is one we should process
                        if extension.lower() in allowed_extensions:
                            self.file_list.append({
                                "path": os.path.join(folder, file_name),
                                "new_name": current_map_lower[file_id.lower()],
                                "id": file_id
                            })
                        else:
                            self.log_message(f"Skipped file (extension invalid): {file_name}")
                    else:
                        self.log_message(f"Skipped file '{file_name}': ID '{file_id}' not found in the selected CSV map.")
        
        total_files = len(self.file_list)
        if total_files == 0:
            messagebox.showinfo("No Files", "No files to rename based on the provided dictionaries and selection.")
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
                
                # Check if the destination file already exists
                if os.path.exists(new_file_path):
                    log_message = f"Skipped: {os.path.basename(new_file_path)} already exists."
                    self.log_message(log_message)
                    logging.warning(log_message)
                    continue

                os.rename(file_data["path"], new_file_path)
                log_message = f"Renamed {file_data['id']}{original_extension} to {os.path.basename(new_file_path)}"
                self.log_message(log_message)
                logging.info(log_message)
            except PermissionError as e:
                log_message = f"Failed to rename {file_data['path']}: Access is denied. The file may be in use. Please close any programs like Unreal Engine or Wwise."
                self.log_message(log_message)
                logging.error(log_message)
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
        selected_type = self.file_type_var.get()
        
        # The list of file extensions to process
        allowed_extensions = ['.uasset', '.uexp', '.ubulk', '.wav']


        if not root_folder or not os.path.isdir(root_folder):
            messagebox.showerror("Error", "Please select a valid work folder.")
            return
        
        if not media_csv_path and not localized_csv_path:
            messagebox.showerror("Error", "Please select at least one CSV file to proceed.")
            return

        media_map_lower = {}
        localized_map_lower = {}
        if media_csv_path and os.path.exists(media_csv_path):
            _, media_map_lower = self.load_name_to_id_map_from_csv(media_csv_path)
            if media_map_lower is None: return

        if localized_csv_path and os.path.exists(localized_csv_path):
            _, localized_map_lower = self.load_name_to_id_map_from_csv(localized_csv_path)
            if localized_map_lower is None: return

        self.update_status("Finding audio folders for reversion...")
        self.log_message("Starting audio file reversion process...")

        audio_folders = self.find_audio_folders(root_folder)
        
        if not audio_folders:
            messagebox.showinfo("No Folders Found", "Could not find 'Media' or 'Localized/English_US_/Media' folders within the selected directory. Please ensure you have selected the main 'PAYDAY3' folder.")
            self.update_status("Reversion cancelled. No audio folders found.")
            return

        self.file_list = []
        for folder in audio_folders:
            is_localized_folder = "Localized" in os.path.normpath(folder)

            current_map_lower = None
            if selected_type == "All":
                current_map_lower = localized_map_lower if is_localized_folder else media_map_lower
            elif selected_type == "Localized (VO)" and is_localized_folder:
                current_map_lower = localized_map_lower
            elif selected_type == "Media (Audio)" and not is_localized_folder:
                current_map_lower = media_map_lower

            if current_map_lower:
                for file_name in os.listdir(folder):
                    file_name_no_ext, extension = os.path.splitext(file_name)
                    # Strip any leading/trailing whitespace from the filename
                    file_name_no_ext = file_name_no_ext.strip()
                    if file_name_no_ext.lower() in current_map_lower:
                        if extension.lower() in allowed_extensions:
                            self.file_list.append({
                                "path": os.path.join(folder, file_name),
                                "original_id": current_map_lower[file_name_no_ext.lower()],
                                "current_name": file_name_no_ext
                            })
                        else:
                            self.log_message(f"Skipped file (extension invalid): {file_name}")
                    else:
                        self.log_message(f"Skipped file '{file_name}': Name '{file_name_no_ext}' not found in the selected CSV map.")

        total_files = len(self.file_list)
        if total_files == 0:
            messagebox.showinfo("No Files", "No files were found to revert based on the provided dictionaries and selection.")
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
                
                # Check if the destination file already exists
                if os.path.exists(new_file_path):
                    log_message = f"Skipped: {os.path.basename(new_file_path)} already exists."
                    self.log_message(log_message)
                    logging.warning(log_message)
                    continue
                
                os.rename(file_data["path"], new_file_path)
                log_message = f"Reverted {file_data['current_name']}{original_extension} to {os.path.basename(new_file_path)}"
                self.log_message(log_message)
                logging.info(log_message)
            except PermissionError as e:
                log_message = f"Failed to revert {file_data['path']}: Access is denied. The file may be in use. Please close any programs like Unreal Engine or Wwise."
                self.log_message(log_message)
                logging.error(log_message)
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
