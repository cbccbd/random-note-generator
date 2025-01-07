import tkinter as tk
import random
import os
import sys
import pyaudio
import time
import threading
from pydub import AudioSegment

# List of music notes and corresponding sound files
music_notes_dict       = {'C': 1, 'C#': 2, 'D': 3, 'D#': 4, 'E': 5, 'F': 6, 'F#': 7, 'G': 8, 'G#': 9, 'A': 10, 'A#': 11, 'B': 12}
music_notes_dict_flats = {'C#': 'Db', 'D#': 'Eb', 'F#': 'Gb', 'G#': 'Ab', 'A#': 'Bb'}
flats_to_sharps_dict   = dict((v, k) for k, v in music_notes_dict_flats.items())
music_notes            = list(music_notes_dict.keys())
sound_files            = {note: f"{note}3 note.wav" for note in music_notes}

# Global variables to manage sound playback and current state
is_playing = False      # To store playing status
current_note = None     # To store current note container
audio_segment = None    # To hold the audio segment for playback
volume_level = 0        # Initial volume level in dB
last_note = None        # To track the last generated note
is_muted = False        # Track mute state
saved_volume_level = 0  # To store the volume level before muting


def play_sound():
    """Play the sound of the specified note in a loop until stopped."""
    global is_playing

    # Open a stream to play the sound with correct parameters
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=2,  # Change to 2 if your audio files are stereo
                    rate=44100,  # Ensure this matches your audio file's sample rate
                    output=True)

    # Read data in chunks and play it until stopped
    while is_playing:
        # Adjust volume in real-time based on the slider value or mute state
        adjusted_audio = audio_segment.apply_gain(volume_level if not is_muted else -100)  # Mute if is_muted

        # Get raw data for playback
        data = adjusted_audio.raw_data

        # Play data in chunks to avoid buffer issues
        chunk_size = 1024  # Define chunk size for playback

        for i in range(0, len(data), chunk_size):
            stream.write(data[i:i + chunk_size])

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()


def stop_sound():
    """Stop any currently playing sound."""
    global is_playing
    is_playing = False


def generate_note_and_start_timer():
    """Generate a random music note, update the label, and start the timer."""
    global current_note, audio_segment, last_note

    stop_sound()  # Stop any currently playing sound before generating a new note

    # Generate a new note that is different from the last one
    while True:
        current_note = random.choice(music_notes)
        if current_note != last_note:
            break

    # If the current half-note is lower than any previous then display as flat(b) otherwise keep sharp(#)
    if last_note:
        if ('#' in current_note) and (music_notes_dict[current_note] < music_notes_dict[last_note]):
            current_note_label = music_notes_dict_flats[current_note]
        else:
            current_note_label = current_note

    # First note handler
    try:
        note_label.config(text=current_note_label)
    except:
        note_label.config(text=current_note)

    # Make flats sharp again
    try:
        current_note = flats_to_sharps_dict[current_note]
    except:
        pass

    # Load the audio file once for playback
    sound_file_path = os.path.join(base_path, sound_files[current_note])

    # Load audio segment once without applying gain here
    audio_segment = AudioSegment.from_wav(sound_file_path)

    # Update last_note to current_note for future checks
    last_note = current_note

    # Start timer for user-defined duration or default to 5 seconds
    try:
        duration = int(timer_entry.get())
        countdown(duration)
    except ValueError:
        note_label.config(text="Invalid input!")


def countdown(duration):
    """Countdown timer logic."""
    global is_playing

    generate_button.config(state=tk.DISABLED)  # Disable button while timer is running

    for remaining in range(duration, -1, -1):
        print(f"remaining: {remaining}")
        timer_label.config(text=f"Time left: {remaining} seconds")
        root.update()  # Update the GUI
        time.sleep(1)  # Wait for 1 second before continuing

    timer_label.config(text="Time left: 0 seconds")

    is_playing = True
    threading.Thread(target=play_sound, daemon=True).start()
    time.sleep(2)

    generate_button.config(state=tk.NORMAL)  # Re-enable button after timer ends


def set_volume(value):
    """Set the volume level based on slider input."""
    global volume_level
    volume_level = int(value)  # Convert slider value to integer


def toggle_mute():
    """Toggle mute state and update button text."""
    global is_muted, saved_volume_level

    if not is_muted:
        saved_volume_level = volume_level
        is_muted = True

        mute_button.config(text="Unmute")
        volume_slider.set(-100)
        set_volume(-100)

    else:
        is_muted = False

        mute_button.config(text="Mute")
        volume_slider.set(saved_volume_level)
        set_volume(saved_volume_level)

    # Create the main window


root = tk.Tk()
root.title("Random Music Note Generator")

# Set window size (width x height)
root.geometry("500x630")

# Determine base path for sound files
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.realpath('__file__'))

# Create a label to display the note
note_label = tk.Label(root, text="", font=("Helvetica", 72), padx=20, pady=20)
note_label.pack(pady=20)

# Create a label for the timer display
timer_label = tk.Label(root, text="Time left: 0 seconds", font=("Helvetica", 24))
timer_label.pack(pady=20)

# Create a text entry for timer adjustment
timer_entry = tk.Entry(root, font=("Helvetica", 24))
timer_entry.insert(0, "5")
timer_entry.pack(pady=20)

# Create a button to generate a new note and start the timer
generate_button = tk.Button(root, text="Generate Note & Start Timer", command=generate_note_and_start_timer,
                            font=("Helvetica", 24))
generate_button.pack(pady=10)

# Create a button to stop playing sound
stop_sound_button = tk.Button(root, text="Stop Playing", command=stop_sound, font=("Helvetica", 24))
stop_sound_button.pack(pady=10)

# Create a frame for volume control and mute button placement
volume_frame = tk.Frame(root)
volume_frame.pack(pady=20)

# Create a slider for volume control (range from -30 dB to +10 dB)
volume_slider = tk.Scale(volume_frame, from_=-30, to=10, orient=tk.HORIZONTAL, label="Volume (dB)", command=set_volume)
volume_slider.set(0)
volume_slider.pack(side=tk.LEFT)

# Create a button for muting/unmuting audio next to the volume slider
mute_button = tk.Button(volume_frame, text="Mute", command=toggle_mute, font=("Helvetica", 24))
mute_button.pack(side=tk.LEFT)

# Start the GUI event loop
root.mainloop()
