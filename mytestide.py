import tkinter as tk
from tkinter import ttk
from browser_action import BrowserActions
from datetime import datetime
import threading
from typing import List

class MyTestIDE(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MyTestIDE")
        self.geometry("600x400")

        # Initialize BrowserActions
        self.browser_actions = BrowserActions()

        # UI components
        self.record_button = ttk.Button(self, text="Record", command=self.start_recording)
        self.record_button.pack()

        self.stop_button = ttk.Button(self, text="Stop", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack()

        self.save_button = ttk.Button(self, text="Save", command=self.save_actions, state=tk.DISABLED)
        self.save_button.pack()

        self.play_button = ttk.Button(self, text="Play", command=self.play_actions, state=tk.DISABLED)
        self.play_button.pack()

        self.action_listbox = tk.Listbox(self, height=15, width=70)
        self.action_listbox.pack()

        self.recording_label = tk.Label(self, text="", fg="red", font=("Arial", 12, "bold"))
        self.recording_label.pack()

        self.start_time: datetime = None
        self.update_timer()

    def start_recording(self):
        """Start recording actions."""
        self.browser_actions.start_recording()
        self.start_time = datetime.now()
        self.set_recording_label("Recording Started")
        self.record_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.save_button.config(state=tk.DISABLED)
        self.play_button.config(state=tk.DISABLED)

    def stop_recording(self):
        """Stop recording actions."""
        self.browser_actions.stop_recording()
        self.start_time = None 
        self.set_recording_label("")
        self.record_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.NORMAL)
        self.play_button.config(state=tk.NORMAL)
        self.refresh_action_listbox()

    def save_actions(self):
        """Save recorded actions."""
        self.browser_actions.save_actions()
        self.refresh_action_listbox()

    def play_actions(self):
        """Play recorded actions."""
        threading.Thread(target=self.execute_recorded_actions).start()

    def execute_recorded_actions(self):
        """Execute recorded actions."""
        actions: List[str] = self.browser_actions.get_actions()
        for action in actions:
            self.execute_recorded_action(action)

    def execute_recorded_action(self, action: str):
        """Execute a single recorded action."""
        if action.startswith("get"):
            url = action.split(" ")[1]
            self.browser_actions.driver.get(url)
        elif action.startswith("click"):
            locator = action.split(" ")[1]
            element = self.browser_actions.driver.find_element_by_css_selector(locator)
            element.click()
        elif action.startswith("type"):
            locator, text = action.split(" ")[1:]
            element = self.browser_actions.driver.find_element_by_css_selector(locator)
            element.send_keys(text)
        time.sleep(2)  # Add a delay between actions

    def refresh_action_listbox(self):
        """Refresh the action listbox."""
        self.action_listbox.delete(0, tk.END)
        actions: List[str] = self.browser_actions.get_actions()
        for action in actions:
            self.action_listbox.insert(tk.END, action)

    def set_recording_label(self, text: str):
        """Set the recording label."""
        self.recording_label.config(text=text)

    def update_timer(self):
        """Update the recording timer."""
        if self.start_time:
            elapsed_time = datetime.now() - self.start_time
            self.recording_label.config(text=f"Recording Started: {elapsed_time}")
        self.after(1000, self.update_timer)

if __name__ == "__main__":
    app = MyTestIDE()
    app.mainloop()
