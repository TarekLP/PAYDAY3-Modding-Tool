# tabs/music_tab.py
import tkinter as tk
from tkinter import ttk
import logging
import pygame
import os
import random

# The MusicPlayer class handles the backend logic for music playback.
class MusicPlayer:
    """
    A class to handle background music playback.
    """
    def __init__(self, music_dir, initial_volume=0.5):
        self.music_dir = music_dir
        self.music_files = []
        self.is_playing = False
        self.is_paused = False
        self.current_volume = initial_volume
        self.current_song_name = "None"
        try:
            pygame.mixer.init()
        except pygame.error as e:
            logging.error(f"Could not initialize Pygame mixer: {e}")
            self.is_playing = False

    def load_music_from_folder(self):
        """
        Scans the music folder and its subfolders for supported audio files.
        """
        if not os.path.exists(self.music_dir):
            logging.warning("Music folder not found. Creating it.")
            os.makedirs(self.music_dir)
            return
            
        self.music_files = []
        for root, _, files in os.walk(self.music_dir):
            for filename in files:
                if filename.lower().endswith(('.mp3', '.wav', '.ogg', '.flac')):
                    self.music_files.append(os.path.join(root, filename))

    def play_random_song(self):
        """
        Plays a random song from the loaded music files.
        """
        if not self.music_files:
            logging.warning("No music files found to play.")
            return

        song_path = random.choice(self.music_files)
        try:
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.set_volume(self.current_volume)
            pygame.mixer.music.play(-1)  # Loop indefinitely
            self.is_playing = True
            self.is_paused = False
            self.current_song_name = os.path.basename(song_path)
        except pygame.error as e:
            logging.error(f"Could not play song {song_path}: {e}")
            self.is_playing = False
            self.is_paused = False
            self.current_song_name = "Error"
        
    def play_music(self):
        """
        Starts or resumes music playback.
        """
        # If the music is paused, unpause it.
        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_playing = True
            self.is_paused = False
        # If it's not playing (and not paused), it must be stopped, so start a new song.
        elif not self.is_playing:
            self.play_random_song()

    def pause_music(self):
        """
        Pauses the music playback.
        """
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.is_playing = False
            self.is_paused = True

    def stop_music(self):
        """
        Stops the music entirely.
        """
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
        self.current_song_name = "None"

    def set_volume(self, volume):
        """
        Sets the music volume.
        """
        self.current_volume = volume
        pygame.mixer.music.set_volume(volume)

    def get_is_playing(self):
        """
        Returns the current playback state.
        """
        return self.is_playing

    def get_current_song_name(self):
        """
        Returns the name of the currently playing song.
        """
        return self.current_song_name

# The MusicTab class handles the UI elements and controls the MusicPlayer.
class MusicTab(ttk.Frame):
    """
    A tab to control the background music player.
    """
    def __init__(self, parent, root, music_volume=0.5, **kwargs):
        super().__init__(parent, **kwargs)
        self.root = root
        self.status_bar = None
        # Initialize the MusicPlayer instance directly within the tab
        music_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'utils', 'Music')
        self.music_player = MusicPlayer(music_dir, initial_volume=music_volume)
        self.music_player.load_music_from_folder()

        # Attributes for the visualizer
        self.visualizer_bars = []
        self.animation_id = None
        self.num_bars = 30  # Number of bars in the visualizer

        self.create_widgets()
        # Update UI initially
        self.update_music_ui()

    def create_widgets(self):
        """
        Creates and lays out the widgets for the music player tab.
        """
        glass_box = ttk.Frame(self, style='TFrame', padding=(15, 15), relief='groove', borderwidth=2)
        glass_box.pack(expand=True, fill="both", padx=10, pady=10)
        
        # --- Music Control Section ---
        # Using a standard Frame with a relief to create a bordered container.
        # A separate Label is used for the title to allow for centering and avoid potential rendering issues.
        music_frame = ttk.Frame(glass_box, style='TFrame', padding=(10, 10), relief='groove', borderwidth=1)
        music_frame.pack(pady=20, fill='x', padx=20)

        title_label = ttk.Label(music_frame, text="Background Music", style='TLabel', font=("Helvetica", 12, "bold"), anchor='center')
        title_label.pack(pady=(0, 10), fill='x')

        # Music status label
        self.music_status_label = ttk.Label(music_frame, text="Music: Not Loaded", style='TLabel', anchor='center')
        self.music_status_label.pack(pady=(0, 15), fill='x')

        # Visualizer Canvas
        self.visualizer_canvas = tk.Canvas(music_frame, height=60, bg='#2a2a2a', highlightthickness=0)
        self.visualizer_canvas.pack(fill='x', pady=(0, 15), padx=10)
        self.visualizer_canvas.bind("<Configure>", self.on_canvas_resize)
        
        # Play/Pause and Stop buttons
        control_frame = ttk.Frame(music_frame, style='TFrame')
        control_frame.pack(pady=(0, 10))
        
        self.play_pause_button = ttk.Button(control_frame, text="Play", command=self.toggle_music, style='TButton', width=10)
        self.play_pause_button.pack(side='left', padx=5)
        
        self.stop_button = ttk.Button(control_frame, text="Stop", command=self.stop_music, style='TButton', width=10)
        self.stop_button.pack(side='left', padx=5)
        
        # Volume control slider
        volume_frame = ttk.Frame(music_frame, style='TFrame')
        volume_frame.pack(pady=10, fill='x', padx=20)

        volume_label = ttk.Label(volume_frame, text="Volume:", style='TLabel')
        volume_label.pack(side='left', padx=(0, 10))

        self.volume_slider = ttk.Scale(
            volume_frame,
            from_=0,
            to=1,
            orient="horizontal",
            command=self.set_volume
        )
        self.volume_slider.pack(side='left', expand=True, fill='x')

    def on_canvas_resize(self, event):
        """Redraws the visualizer bars when the canvas is resized."""
        self.init_visualizer_bars()

    def init_visualizer_bars(self):
        """Initializes or re-initializes the visualizer bars."""
        self.visualizer_canvas.delete("all")
        self.visualizer_bars = []
        
        canvas_width = self.visualizer_canvas.winfo_width()
        canvas_height = self.visualizer_canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            self.after(50, self.init_visualizer_bars)
            return

        bar_width = canvas_width / self.num_bars
        spacing = bar_width * 0.3
        actual_bar_width = bar_width - spacing

        for i in range(self.num_bars):
            x0 = i * bar_width + (spacing / 2)
            y0 = canvas_height
            x1 = x0 + actual_bar_width
            y1 = canvas_height - 2 # Minimum height
            bar = self.visualizer_canvas.create_rectangle(x0, y0, x1, y1, fill='#4a663b', outline="")
            self.visualizer_bars.append(bar)

    def start_visualizer_animation(self):
        """Starts the visualizer animation loop."""
        if self.animation_id:
            return  # Already running
        self.animate_visualizer()

    def stop_visualizer_animation(self):
        """Stops the visualizer animation loop and resets bars."""
        if self.animation_id:
            self.after_cancel(self.animation_id)
            self.animation_id = None
        
        if not self.visualizer_bars: return

        canvas_height = self.visualizer_canvas.winfo_height()
        for bar in self.visualizer_bars:
            coords = self.visualizer_canvas.coords(bar)
            if coords:
                x0, _, x1, _ = coords
                self.visualizer_canvas.coords(bar, x0, canvas_height, x1, canvas_height - 2)

    def animate_visualizer(self):
        """The core animation function, called repeatedly."""
        if not self.music_player.is_playing:
            self.stop_visualizer_animation()
            return

        canvas_height = self.visualizer_canvas.winfo_height()
        if canvas_height <= 1:  # Canvas not ready yet
            self.animation_id = self.after(100, self.animate_visualizer)
            return

        for bar in self.visualizer_bars:
            coords = self.visualizer_canvas.coords(bar)
            if coords:
                x0, _, x1, _ = coords
                new_height = random.randint(2, canvas_height)
                self.visualizer_canvas.coords(bar, x0, canvas_height, x1, canvas_height - new_height)
        
        self.animation_id = self.after(100, self.animate_visualizer)

    def update_music_ui(self):
        """
        Updates the UI elements based on the current music state.
        """
        if self.music_player:
            self.volume_slider.set(self.music_player.current_volume)
            
            if self.music_player.is_playing:
                self.music_status_label.config(text=f"Now Playing: {self.music_player.current_song_name}")
                self.play_pause_button.config(text="Pause")
                self.stop_button.config(state='normal')
                self.start_visualizer_animation()
            else:
                try:
                    is_stopped = pygame.mixer.music.get_pos() == -1
                except pygame.error:
                    is_stopped = True

                if is_stopped:
                    self.music_status_label.config(text="Music is Stopped")
                    self.stop_button.config(state='disabled')
                else:
                    self.music_status_label.config(text="Music is Paused")
                    self.stop_button.config(state='normal')
                
                self.play_pause_button.config(text="Play")
                self.stop_visualizer_animation()
            
            if not self.music_player.music_files:
                self.music_status_label.config(text="Music: No files found in utils/Music")
                self.play_pause_button.config(state='disabled')
                self.stop_button.config(state='disabled')

    def toggle_music(self):
        """Toggles music playback on and off."""
        if self.music_player:
            if self.music_player.is_playing:
                self.music_player.pause_music()
            else:
                self.music_player.play_music()
            self.update_music_ui()
            self.root.save_preferences(music_is_playing=self.music_player.is_playing)

    def stop_music(self):
        """Stops the music entirely."""
        if self.music_player:
            self.music_player.stop_music()
            self.update_music_ui()
            self.root.save_preferences(music_is_playing=False)

    def set_volume(self, value):
        """Sets the music volume based on the slider value."""
        if self.music_player:
            self.music_player.set_volume(float(value))
            self.root.save_preferences(music_volume=self.music_player.current_volume)
