# utils/tooltip.py
import tkinter as tk

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.id = None
        self.x = 0
        self.y = 0
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hide()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(500, self.show)

    def unschedule(self):
        if self.id:
            self.widget.after_cancel(self.id)
            self.id = None

    def show(self):
        self.x = self.widget.winfo_rootx() + 25
        self.y = self.widget.winfo_rooty() + 25
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{self.x}+{self.y}")

        label = tk.Label(self.tooltip_window, text=self.text, background="#ffffc6", relief="solid", borderwidth=1, font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide(self):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None