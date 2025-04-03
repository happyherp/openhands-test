import json
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def select_and_load_json():
    """Open a file dialog to select a JSON file and load its content."""
    Tk().withdraw()  # Hide the root Tkinter window
    file_path = askopenfilename(
        title="Select JSON File",
        filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
    )
    if not file_path:
        raise FileNotFoundError("No file selected.")
    
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
