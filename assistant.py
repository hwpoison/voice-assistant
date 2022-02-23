#!/usr/bin/env python3
import os
import queue
import sounddevice as sd
import vosk
import sys
import json 

import processor 
import commands

audio_blocks_queue = queue.Queue()

DEVICE_INPUT_NUMBER = None
if not DEVICE_INPUT_NUMBER:
    print("Available inputs devices, please select your input device (choice with '>' symbol):")
    print(sd.query_devices())
    DEVICE_INPUT_NUMBER = int(input("[INPUT DEVICE NUMBER]:"))

# status
DONE_COMMAND = False # check success cmd
PREV_SENTENCE = None # prevents repeat

def analize_entry(entry):
    global PREV_SENTENCE, DONE_COMMAND
    if entry and PREV_SENTENCE != entry:
        print(f"[i] Analyzing entry '{entry}'")
        DONE_COMMAND = False
        if entry in commands.again_words:
            processor.repeat_last_command()
        else:
            processor.run_command(entry)
        DONE_COMMAND = True
        PREV_SENTENCE = entry

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    audio_blocks_queue.put(bytes(indata))

try:
    model = "model"
    device_info = sd.query_devices(DEVICE_INPUT_NUMBER, 'input')
    # soundfile expects an int, sounddevice provides a float:
    samplerate = int(device_info['default_samplerate'])
    model = vosk.Model(model)
    with sd.RawInputStream(samplerate=samplerate, blocksize = 8000, device=DEVICE_INPUT_NUMBER, dtype='int16',
                            channels=1, callback=callback):
        print('#' * 80)
        print('Ready, press Ctrl+C to stop listening...')
        print('#' * 80)
        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = audio_blocks_queue.get() # get audio block from queue
            if rec.AcceptWaveform(data): # final sentence
                text = rec.Result()
                text_json = json.loads(text)
                if(full_entry:= text_json["text"]):
                    # Reset previous sentence
                    PREV_SENTENCE = "" 
                    if not DONE_COMMAND:
                        # process total and corrected input sentence
                        # if partial result is not conclusive
                        print("[i] Analyzing entire entry")
                        analize_entry(full_entry)
                    # Reset model TODO: fix memory leak ( .Reset() method apparently not working )
                    rec = vosk.KaldiRecognizer(model, samplerate) 
            else:
                partial = rec.PartialResult() # partial sentence
                partial_json = json.loads(partial)
                if(partial_entry := partial_json.get("partial")):
                    #print("[!]Partial entry:", partial_entry)
                    # process partial input
                    analize_entry(partial_entry)
                    
except KeyboardInterrupt:
    print('\nDone')
    sys.exit(0)
except Exception as e:
    sys.exit(type(e).__name__ + ': ' + str(e))