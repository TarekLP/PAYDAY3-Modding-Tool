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

        form_frame = ttk.Frame(glass_box, style='TFrame', padding=(20, 20))
        form_frame.pack(fill='both', expand=True)

        self.mod_name_var = tk.StringVar()
        self.mod_version_var = tk.StringVar()
        self.icon_file_path_var = tk.StringVar()
        
        # --- Mod Information Section ---
        ttk.Label(form_frame, text="MOD INFORMATION", style='TLabel', font=("Helvetica", 14, "bold")).grid(row=0, column=0, columnspan=2, sticky='w', pady=(0, 5))
        
        # Mod Name
        ttk.Label(form_frame, text="Mod Name:", style='TLabel').grid(row=1, column=0, sticky='w', pady=5)
        ttk.Entry(form_frame, textvariable=self.mod_name_var, width=50).grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        # Mod Authors (now multi-line)
        ttk.Label(form_frame, text="Mod Authors:", style='TLabel').grid(row=2, column=0, sticky='w', pady=5)
        self.mod_author_text = tk.Text(form_frame, height=3, width=40, bg='#333333', fg='white', relief='flat')
        self.mod_author_text.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(form_frame, text="Separate authors by new line.", style='TLabel', foreground="#999999", font=("Helvetica", 8)).grid(row=3, column=1, sticky='w', padx=5)

        # Mod Version
        ttk.Label(form_frame, text="Mod Version:", style='TLabel').grid(row=4, column=0, sticky='w', pady=5)
        ttk.Entry(form_frame, textvariable=self.mod_version_var, width=50).grid(row=4, column=1, padx=5, pady=5, sticky='ew')

        # Mod Description
        ttk.Label(form_frame, text="Mod Description:", style='TLabel').grid(row=5, column=0, sticky='w', pady=5)
        self.mod_description_text = tk.Text(form_frame, height=5, width=40, bg='#333333', fg='white', relief='flat')
        self.mod_description_text.grid(row=5, column=1, padx=5, pady=5, sticky='ew')
        
        # --- Separator ---
        ttk.Separator(form_frame, orient='horizontal').grid(row=6, column=0, columnspan=2, sticky='ew', pady=15)
        
        # --- Mod Files Section ---
        ttk.Label(form_frame, text="MOD FILES", style='TLabel', font=("Helvetica", 14, "bold")).grid(row=7, column=0, columnspan=2, sticky='w', pady=(0, 5))
        
        # Icon File
        icon_frame = ttk.Frame(form_frame, style='TFrame')
        icon_frame.grid(row=8, column=0, columnspan=2, sticky='ew', pady=5)

        ttk.Label(icon_frame, text="Icon File:", style='TLabel').pack(side='left', padx=(0, 5))
        ttk.Entry(icon_frame, textvariable=self.icon_file_path_var, width=40).pack(side='left', expand=True, fill='x', padx=(0, 5))
        ttk.Button(icon_frame, text="Browse", command=self.browse_icon_file, width=15).pack(side='left')

        # PAK File List
        pak_frame = ttk.Frame(form_frame, style='TFrame')
        pak_frame.grid(row=9, column=0, columnspan=2, sticky='ew', pady=5)

        ttk.Label(pak_frame, text=".PAK Files:", style='TLabel').pack(side='left', anchor='n', padx=(0, 0))

        listbox_frame = ttk.Frame(pak_frame, style='TFrame')
        listbox_frame.pack(side='left', expand=True, fill='both')

        self.pak_listbox = tk.Listbox(listbox_frame, selectmode='multiple', bg='#333333', fg='white', relief='flat', height=5, selectbackground=GREEN, selectforeground='black')
        self.pak_listbox.pack(side='left', fill='both', expand=True)

        
        # Buttons for PAK listbox
        pak_buttons_frame = ttk.Frame(pak_frame, style='TFrame')
        pak_buttons_frame.pack(side='right', fill='y', padx=5)
        
        ttk.Button(pak_buttons_frame, text="Add PAKs", command=self.add_pak_files, width=15).pack(pady=2, fill='x')
        ttk.Button(pak_buttons_frame, text="Remove Selected", command=self.remove_pak_files, width=15).pack(pady=2, fill='x')

        # Generate Button
        generate_button = ttk.Button(form_frame, text="Create Mod", command=self.create_mod, width=25)
        generate_button.grid(row=10, column=0, columnspan=2, pady=20)
        
        # Save/Load Profile Buttons
        profile_buttons_frame = ttk.Frame(glass_box, style='TFrame')
        profile_buttons_frame.pack(fill='x', pady=10)
        ttk.Button(profile_buttons_frame, text="Save Profile", command=self.save_profile, width=20).pack(side='left', expand=True, padx=(0, 5))
        ttk.Button(profile_buttons_frame, text="Load Profile", command=self.load_profile, width=20).pack(side='right', expand=True, padx=(5, 0))

        form_frame.columnconfigure(1, weight=1)

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

