import json
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os
import webbrowser

# Define cost rates in USD per token (per million tokens)
COST_PER_COMPLETION_TOKEN = 15.00 / 1000 / 1000
COST_PER_CACHE_WRITE_TOKEN = 3.75 / 1000 / 1000
COST_PER_CACHE_READ_TOKEN = 0.30 / 1000 / 1000

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



def save_and_open_html(html_content, filename):
    """Save HTML content to a file and open it in the default web browser."""
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, filename)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    webbrowser.open(output_file)
