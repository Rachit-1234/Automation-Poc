from selenium import webdriver
import time
from typing import List

class BrowserActions:
    def __init__(self):
        self.actions: List[str] = []
        self.recording: bool = False

    def start_recording(self):
        """Start recording actions."""
        self.actions.clear()
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.geeksforgeeks.org/courses?source=google&medium=cpc&device=c&keyword=geeksforgeeks&matchtype=e&campaignid=20039445781&adgroup=147845288105&gad_source=1&gclid=EAIaIQobChMItJ_OqoLvhQMV2WwPAh27Mwi1EAAAYASAAEgLH0_D_BwE")
        self.driver.maximize_window()
        self.recording = True

    def stop_recording(self):
        """Stop recording actions."""
        self.recording = False
        self.driver.quit()

    def save_actions(self, filename: str = "recorded_actions.txt"):
        """Save recorded actions to a file."""
        with open(filename, "w") as f:
            for action in self.actions:
                f.write(action + "\n")

    def play_actions(self, filename: str = "recorded_actions.txt"):
        """Play recorded actions from a file."""
        self.driver = webdriver.Chrome()
        with open(filename, "r") as f:
            for line in f:
                action = line.strip()
                self.execute_action(action)
        self.driver.quit()

    def execute_action(self, action: str):
        """Execute a single recorded action."""
        if action.startswith("get"):
            url = action.split(" ")[1]
            self.driver.get(url)
        elif action.startswith("click"):
            locator = action.split(" ")[1]
            element = self.driver.find_element_by_css_selector(locator)
            element.click()
        elif action.startswith("type"):
            locator, text = action.split(" ")[1:]
            element = self.driver.find_element_by_css_selector(locator)
            element.send_keys(text)
        time.sleep(2)
        self.actions.append(action)

    def get_actions(self) -> List[str]:
        """Get the list of recorded actions."""
        return self.actions.copy()
