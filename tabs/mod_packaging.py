# tabs/mod_packaging.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import shutil
import json
import logging
import zipfile

# PD3 green accent
GREEN = "#62854f"

class ModPackagingTab(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.status_bar = None
        self.create_widgets()
        self.load_profile()

    def create_widgets(self):
        glass_box = ttk.Frame(self, style='TFrame', padding=(15, 15), relief='groove', borderwidth=2)
        glass_box.pack(expand=True, fill="both", padx=10, pady=10)

        # --- Mod Information Section ---
        info_frame = ttk.Frame(glass_box, style='TFrame', padding=(10, 10), relief='groove', borderwidth=1)
        info_frame.pack(fill='x', pady=(0, 10))
        
        info_title = ttk.Label(info_frame, text="Mod Information", style='TLabel', font=("Helvetica", 12, "bold"))
        info_title.pack(anchor='w', pady=(0, 10))

        # Row for Mod Name
        name_frame = ttk.Frame(info_frame, style='TFrame')
        name_frame.pack(fill='x', pady=3)
        ttk.Label(name_frame, text="Mod Name:", style='TLabel', width=15).pack(side='left')
        self.mod_name_var = tk.StringVar()
        ttk.Entry(name_frame, textvariable=self.mod_name_var).pack(side='left', expand=True, fill='x')

        # Row for Mod Authors
        authors_frame = ttk.Frame(info_frame, style='TFrame')
        authors_frame.pack(fill='x', pady=3, anchor='n')
        ttk.Label(authors_frame, text="Mod Authors:", style='TLabel', width=15).pack(side='left', anchor='n', pady=3)
        self.mod_author_text = tk.Text(authors_frame, height=3, width=40, bg='#333333', fg='white', relief='flat', font=('Helvetica', 10), insertbackground='white')
        self.mod_author_text.pack(side='left', expand=True, fill='x')
        
        # Help text for authors
        authors_help_frame = ttk.Frame(info_frame, style='TFrame')
        authors_help_frame.pack(fill='x', pady=(0, 5))
        ttk.Label(authors_help_frame, text="", width=15).pack(side='left') # Spacer
        ttk.Label(authors_help_frame, text="Separate authors by new line.", style='TLabel', foreground="#999999", font=("Helvetica", 8)).pack(side='left')

        # Row for Mod Version
        version_frame = ttk.Frame(info_frame, style='TFrame')
        version_frame.pack(fill='x', pady=3)
        ttk.Label(version_frame, text="Mod Version:", style='TLabel', width=15).pack(side='left')
        self.mod_version_var = tk.StringVar()
        ttk.Entry(version_frame, textvariable=self.mod_version_var).pack(side='left', expand=True, fill='x')

        # Row for Mod Description
        desc_frame = ttk.Frame(info_frame, style='TFrame')
        desc_frame.pack(fill='x', pady=3, anchor='n')
        ttk.Label(desc_frame, text="Mod Description:", style='TLabel', width=15).pack(side='left', anchor='n', pady=3)
        self.mod_description_text = tk.Text(desc_frame, height=5, width=40, bg='#333333', fg='white', relief='flat', font=('Helvetica', 10), insertbackground='white')
        self.mod_description_text.pack(side='left', expand=True, fill='x')

        # --- Mod Files Section ---
        files_frame = ttk.Frame(glass_box, style='TFrame', padding=(10, 10), relief='groove', borderwidth=1)
        files_frame.pack(fill='x', expand=True, pady=10)

        files_title = ttk.Label(files_frame, text="Mod Files", style='TLabel', font=("Helvetica", 12, "bold"))
        files_title.pack(anchor='w', pady=(0, 10))

        # Row for Icon File
        icon_frame = ttk.Frame(files_frame, style='TFrame')
        icon_frame.pack(fill='x', pady=3)
        ttk.Label(icon_frame, text="Icon File:", style='TLabel', width=15).pack(side='left')
        self.icon_file_path_var = tk.StringVar()
        ttk.Entry(icon_frame, textvariable=self.icon_file_path_var).pack(side='left', expand=True, fill='x', padx=(0, 5))
        ttk.Button(icon_frame, text="Browse", command=self.browse_icon_file).pack(side='left')

        # Row for PAK File List
        pak_frame = ttk.Frame(files_frame, style='TFrame')
        pak_frame.pack(fill='both', expand=True, pady=3)
        ttk.Label(pak_frame, text=".PAK Files:", style='TLabel', width=15).pack(side='left', anchor='n', pady=3)
        
        listbox_container = ttk.Frame(pak_frame, style='TFrame')
        listbox_container.pack(side='left', fill='both', expand=True)
        
        self.pak_listbox = tk.Listbox(listbox_container, selectmode='multiple', bg='#333333', fg='white', relief='flat', height=5, selectbackground=GREEN, selectforeground='black', font=('Helvetica', 10))
        self.pak_listbox.pack(side='left', fill='both', expand=True)

        pak_buttons_frame = ttk.Frame(listbox_container, style='TFrame')
        pak_buttons_frame.pack(side='right', fill='y', padx=(5, 0))
        ttk.Button(pak_buttons_frame, text="Add", command=self.add_pak_files).pack(pady=2, fill='x')
        ttk.Button(pak_buttons_frame, text="Remove", command=self.remove_pak_files).pack(pady=2, fill='x')

        # --- Actions Section ---
        actions_frame = ttk.Frame(glass_box, style='TFrame', padding=(10, 10), relief='groove', borderwidth=1)
        actions_frame.pack(fill='x', pady=(10, 0))

        actions_title = ttk.Label(actions_frame, text="Actions", style='TLabel', font=("Helvetica", 12, "bold"))
        actions_title.pack(anchor='w', pady=(0, 10))

        # A frame to center the main "Create Mod" button
        create_button_frame = ttk.Frame(actions_frame, style='TFrame')
        create_button_frame.pack(fill='x', pady=5)
        ttk.Button(create_button_frame, text="Create Mod", command=self.create_mod).pack()

        ttk.Separator(actions_frame, orient='horizontal').pack(fill='x', pady=10)

        # A frame for the profile buttons
        profile_buttons_frame = ttk.Frame(actions_frame, style='TFrame')
        profile_buttons_frame.pack(fill='x')
        ttk.Button(profile_buttons_frame, text="Save Profile", command=self.save_profile).pack(side='left', expand=True, padx=(0, 5))
        ttk.Button(profile_buttons_frame, text="Load Profile", command=self.load_profile).pack(side='right', expand=True, padx=(5, 0))

    def handle_dnd_drop(self, event):
        files = self.tk.splitlist(event.data)
        for file_path in files:
            if file_path.endswith('.pak'):
                self.pak_listbox.insert(tk.END, file_path)

    def add_pak_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("PAK files", "*.pak")])
        for file_path in file_paths:
            self.pak_listbox.insert(tk.END, file_path)

    def remove_pak_files(self):
        selected_indices = self.pak_listbox.curselection()
        for index in selected_indices[::-1]:
            self.pak_listbox.delete(index)

    def browse_icon_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
        if file_path:
            self.icon_file_path_var.set(file_path)

    def create_mod(self):
        mod_name = self.mod_name_var.get()
        mod_authors_str = self.mod_author_text.get("1.0", tk.END).strip()
        mod_version = self.mod_version_var.get()
        mod_description = self.mod_description_text.get("1.0", tk.END).strip()
        icon_file_path = self.icon_file_path_var.get()
        pak_files = self.pak_listbox.get(0, tk.END)

        if not mod_name or not mod_authors_str or not mod_version:
            messagebox.showerror("Error", "Mod Name, Author, and Version are required.")
            return

        try:
            mods_base_dir = os.path.join(os.getcwd(), "Mods")
            os.makedirs(mods_base_dir, exist_ok=True)

            mod_dir = os.path.join(mods_base_dir, mod_name)
            if os.path.exists(mod_dir):
                shutil.rmtree(mod_dir)
            os.makedirs(mod_dir, exist_ok=True)

            mod_data = {
                "name": mod_name,
                "authors": [author.strip() for author in mod_authors_str.split('\n') if author.strip()],
                "version": mod_version,
                "description": mod_description,
                "paks": []
            }

            # Handle the mod icon
            if icon_file_path and os.path.exists(icon_file_path):
                shutil.copy2(icon_file_path, os.path.join(mod_dir, "icon.png"))
            else:
                default_icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "utils", "icon.png")
                if os.path.exists(default_icon_path):
                    shutil.copy2(default_icon_path, os.path.join(mod_dir, "icon.png"))
            
            if pak_files:
                pak_dir = os.path.join(mod_dir, "paks")
                os.makedirs(pak_dir, exist_ok=True)
                
                for pak_file_path in pak_files:
                    pak_filename = os.path.basename(pak_file_path)
                    destination_pak_path = os.path.join(pak_dir, pak_filename)
                    shutil.copy2(pak_file_path, destination_pak_path)
                    mod_data["paks"].append(os.path.join("paks", pak_filename).replace("\\", "/"))

            json_file_path = os.path.join(mod_dir, "pd3mod.json")
            with open(json_file_path, 'w') as f:
                json.dump(mod_data, f, indent=4)
            
            messagebox.showinfo("Success", "Mod has been created! Check the Mods folder in the Tools Installation Path folder and check if everything is there before packaging it.")
            
        except PermissionError:
            messagebox.showerror("Permission Error", "Could not write files. Please run the tool as an administrator.")
        except FileNotFoundError:
            messagebox.showerror("File Not Found", "One or more files were not found. Please check your paths.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            logging.error(f"Mod packaging error: {e}")

    def save_profile(self):
        profile = {
            "name": self.mod_name_var.get(),
            "authors": self.mod_author_text.get("1.0", tk.END).strip().split('\n'),
            "version": self.mod_version_var.get(),
            "description": self.mod_description_text.get("1.0", tk.END).strip(),
            "icon_path": self.icon_file_path_var.get(),
            "pak_files": self.pak_listbox.get(0, tk.END)
        }
        
        try:
            with open("profile.json", "w") as f:
                json.dump(profile, f, indent=4)
            messagebox.showinfo("Success", "Mod profile saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save profile: {e}")
            logging.error(f"Profile save error: {e}")

    def load_profile(self):
        if not os.path.exists("profile.json"):
            return

        try:
            with open("profile.json", "r") as f:
                profile = json.load(f)
            
            self.mod_name_var.set(profile.get("name", ""))
            self.mod_version_var.set(profile.get("version", ""))
            
            self.mod_author_text.delete("1.0", tk.END)
            self.mod_author_text.insert("1.0", "\n".join(profile.get("authors", [])))
            
            self.mod_description_text.delete("1.0", tk.END)
            self.mod_description_text.insert("1.0", profile.get("description", ""))
            
            self.icon_file_path_var.set(profile.get("icon_path", ""))

            self.pak_listbox.delete(0, tk.END)
            for pak in profile.get("pak_files", []):
                self.pak_listbox.insert(tk.END, pak)
            
            messagebox.showinfo("Success", "Mod profile loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not load profile: {e}")
            logging.error(f"Profile load error: {e}")
