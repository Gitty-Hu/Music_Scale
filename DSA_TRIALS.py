import os
import tkinter as tk
from tkinter import ttk
from pydub import AudioSegment
from pydub.playback import play
import time

# Circular list class to handle wrapping around notes
class CircularList:
    def __init__(self, items):
        self.items = items
    
    def get(self, index):
        # Use the modulus operator to wrap the index
        return self.items[index % len(self.items)]
    
    def get_index(self, ite):
        return self.items.index(ite)

# Note lists for sharp and flat notation
Notes1 = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
Notes2 = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']

# Whole steps and half steps for different scales
SCALES = {
    'MAJOR_SCALE': [2, 2, 1, 2, 2, 2, 1],
    'MINOR_SCALE': [2, 1, 2, 2, 1, 2, 2],
    'HARMONIC_MINOR_SCALE': [2, 1, 2, 2, 1, 3, 1],
    'MELODIC_MINOR_ASCENDING': [2, 1, 2, 2, 2, 2, 1],
    'MELODIC_MINOR_DESCENDING': [2, 1, 2, 2, 1, 2, 2],
    'PENTATONIC_SCALE': [2, 2, 3, 2, 3],
    'BLUES_SCALE': [3, 2, 1, 1, 3, 2],
    'CHROMATIC_SCALE': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    'WHOLE_SCALE': [2, 2, 2, 2, 2, 2]
}

# Function to generate the scale based on inputs
def generate_scale():
    NOTELISTEN = []
    
    note = note_var.get()
    scale = scale_var.get()
    notetype = notetype_var.get()
    
    if notetype == "SHARP":
        circular_notes = CircularList(Notes1)
        start = Notes1.index(note)
    else:
        circular_notes = CircularList(Notes2)
        start = Notes2.index(note)
    
    NOTELISTEN.append(circular_notes.get(start))
    
    for i in SCALES[scale]:
        start += i
        NOTELISTEN.append(circular_notes.get(start))
    
    result_label.config(text="Scale: " + ', '.join(NOTELISTEN))
    play_scale(NOTELISTEN)

# Custom function to play audio using ffplay with a custom temp directory
def _play_with_ffplay(audio_segment):
    # Set a custom temp directory
    custom_temp_dir = "C:/Users/Lenovo/Downloads/DSA_Project/temp"
    os.makedirs(custom_temp_dir, exist_ok=True)  # Ensure the temp directory exists
    temp_file = os.path.join(custom_temp_dir, "temp_audio.wav")
    audio_segment.export(temp_file, format="wav")
    os.system(f'ffplay -nodisp -autoexit {temp_file}')

# Function to play the scale using pydub
def play_scale(notes):
    for note in notes:
        try:
            # Load the audio file for each note and play it
            sound = AudioSegment.from_file(f"sounds/{note}.wav", format="wav")
            _play_with_ffplay(sound)  # Use the custom play function
            time.sleep(0.000000000000000000000000000001)  # Small delay between notes
        except FileNotFoundError:
            print(f"Audio file for note {note} not found.")

# Set up the tkinter window
root = tk.Tk()
root.title("Scale Selector")

# Variables to store selections
note_var = tk.StringVar()
scale_var = tk.StringVar()
notetype_var = tk.StringVar()

# Dropdown for selecting the note
note_label = tk.Label(root, text="Select a Note:")
note_label.pack()
note_dropdown = ttk.Combobox(root, textvariable=note_var, values=Notes1)
note_dropdown.pack()

# Dropdown for selecting the scale
scale_label = tk.Label(root, text="Select a Scale:")
scale_label.pack()
scale_dropdown = ttk.Combobox(root, textvariable=scale_var, values=list(SCALES.keys()))
scale_dropdown.pack()

# Dropdown for selecting sharp or flat
notetype_label = tk.Label(root, text="Select Sharp or Flat:")
notetype_label.pack()
notetype_dropdown = ttk.Combobox(root, textvariable=notetype_var, values=['SHARP', 'FLAT'])
notetype_dropdown.pack()

# Button to generate and show the scale
generate_button = tk.Button(root, text="Generate Scale", command=generate_scale)
generate_button.pack()

# Label to display the generated scale
result_label = tk.Label(root, text="Scale will be displayed here.")
result_label.pack()

# Run the tkinter main loop
root.mainloop()

