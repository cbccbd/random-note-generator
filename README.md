# random-note-generator
Simple tkinter app for helping user to memorize note layout on the instrument

Generates random note, when times is up it plays note in octave number 3
![image](https://github.com/user-attachments/assets/fa81e0b5-01e8-4baa-9f3a-83cc619a7a6f)
It respects accidental of an alteration of a given pitch (After **_A_** will follow **_Ab_** and not **_G#_** and so on)

Repo contains ready to use .exe and raw python script<br>
.py and .wav to check what inside located in **script** folder<br>
.exe is located inside **WinEXE** folder (MacEXE and LinEXE will be added later)

.exe was created with this command: <br>
_pyinstaller --onefile --windowed --add-data "A3 note.wav;." --add-data "A#3 note.wav;." --add-data "B3 note.wav;." --add-data "C3 note.wav;." --add-data "C#3 note.wav;." --add-data "D3 note.wav;." --add-data "D#3 note.wav;." --add-data "E3 note.wav;." --add-data "F3 note.wav;." --add-data "F#3 note.wav;." --add-data "G3 note.wav;." --add-data "G#3 note.wav;." music_note_generator.py_

MD5 hash of .\music_note_generator.exe:
7ff689d47064eff932503aa97bbdb34c

<br>Program itself looks like this:<br>
![image](https://github.com/user-attachments/assets/3f68d728-26a0-40f6-a103-31a160e9cdea)

1. Window where music note are displayed
2. Field that will count the timer down
3. Text box for you to choose how long timer will goes (default is 5 sec)
4. Button to generate random note and start the timer countdown (disabled while timer is running)
5. Stop the note from sounding
6. Adjust the volume of the program in the range of -30 dB to +10 dB
7. Completely mute notes
