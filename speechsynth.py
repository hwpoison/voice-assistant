import os
import playsound 
from gtts import gTTS
from threading import Thread

file_count = 0

def play_sound_file(file, text):
    print(f"[+] Playing text '{text}'")
    playsound.playsound(file)
    os.remove(file)
    

def speech(text, lang="es"):
    global file_count
    file_name = f"file{file_count}.mp3"
    s = gTTS(text=text, lang="es", slow=False)
    s.save(file_name)
    thread = Thread(target=play_sound_file, args=(file_name, text, ))
    thread.start()
    file_count += 1