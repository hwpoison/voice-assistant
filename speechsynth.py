import time
import tempfile
from threading import Thread

import playsound
from gtts import gTTS
from logger import logger
from settings import Settings


def play_sound_file(file, text):
    logger.info(f"Playing text audio '{text}' ( { file } )")
    playsound.playsound(file)


def speech(text, lang=Settings.lang):
    # Generate temporal file
    with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as temp:
        file_name = temp.name

    # Generate synthetized voice
    syntvoice = gTTS(text=text, lang=lang, slow=False)
    syntvoice.save(file_name)

    # Play it in a thread apart
    thread = Thread(target=play_sound_file, args=(file_name, text, ))
    thread.start()


if __name__ == "__main__":
    speech("Hola Mundo! Espero que esté todo en orden :)", "es")
    time.sleep(5)
    speech("Hello world, i hope you fine :) ", "en")
