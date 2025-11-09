import json
import os
import tkinter as tk
from PIL import Image, ImageTk

# File paths
INPUT_JSON = "crawl-data.json"
IMAGES_DIR = "data/images"
OUTPUT_JSON = "crawl-data-annotated.json"

# Fixed color options
COLOR_OPTIONS = [
    "red", "orange", "yellow", "green", "blue", "purple", "pink", "white", "black", "brown"
]

# Load input entries
with open(INPUT_JSON, 'r') as f: 
    entries = json.load(f)

# Load or initialize annotated entries
if os.path.exists(OUTPUT_JSON):
    with open(OUTPUT_JSON, 'r') as f:
        annotated_entries = json.load(f)
        annotated_ids = {entry['url_id'] for entry in annotated_entries}
else:
    annotated_entries = []
    annotated_ids = set()

def save_entry(updated_entry):
    # Append and save the updated entry with new 'prominent-colors'
    annotated_entries.append(updated_entry)
    with open(OUTPUT_JSON, 'w') as f:
        json.dump(annotated_entries, f, indent=2)

def display_entry(entry):
    url_id = entry['url_id']

    # Match image file by URL ID
    matching_files = [f for f in os.listdir(IMAGES_DIR) if f.startswith(f"{url_id}-")]
    if not matching_files:
        print(f"[!] Image not found for url_id {url_id}")
        return

    image_path = os.path.join(IMAGES_DIR, matching_files[0])

    # Setup Tkinter window
    root = tk.Tk()
    root.title(f"Select Colors for ID {url_id}")

    # Load and display the image
    img = Image.open(image_path)
    img.thumbnail((500, 500))
    photo = ImageTk.PhotoImage(img)
    img_label = tk.Label(root, image=photo)
    img_label.pack(pady=10)

    # Color selection buttons
    selected_colors = []
    buttons = {}

    def toggle_color(color):
        if color in selected_colors:
            selected_colors.remove(color)
            buttons[color].config(relief="raised")
        else:
            selected_colors.append(color)
            buttons[color].config(relief="sunken")

    frame = tk.Frame(root)
    frame.pack(pady=5)
    for color in COLOR_OPTIONS:
        btn = tk.Button(frame, text=color, bg=color, width=10,
                        relief="raised", command=lambda c=color: toggle_color(c))
        btn.pack(side="left", padx=2, pady=2)
        buttons[color] = btn

    # Submit and close
    def submit():
        entry['prominent-colors'] = selected_colors  # <-- Overwrite here
        save_entry(entry)
        root.destroy()

    submit_btn = tk.Button(root, text="Submit", command=submit)
    submit_btn.pack(pady=10)

    root.mainloop()

# Process entries
for entry in entries:
    if entry['url_id'] in annotated_ids:
        continue
    display_entry(entry)

print("✅ Annotation complete.")
