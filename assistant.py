#!/usr/bin/env python3
import os
import queue
import sounddevice as sd
import vosk
import sys
import json 
import processor 
import commands

q = queue.Queue()

print("Available inputs devices, please select your input device (choice with '>' symbol):")
print(sd.query_devices())
DEVICE_INPUT_NUMBER = int(input("[INPUT DEVICE NUMBER]:"))

# status
DONE_SENTENCE = False
PREV_SENTENCE = None

def process_entry(entry):
    global PREV_SENTENCE
    if entry and PREV_SENTENCE != entry: # detect hotword and prevent repeat
        if entry in commands.again_words:
            processor.repeat_last_command()
        else:
            processor.run_command(entry)
        PREV_SENTENCE = entry

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))
  
try:
    model = "model"
    device_info = sd.query_devices(DEVICE_INPUT_NUMBER, 'input')
    # soundfile expects an int, sounddevice provides a float:
    samplerate = int(device_info['default_samplerate'])
    model = vosk.Model(model)
    with sd.RawInputStream(samplerate=samplerate, blocksize = 8000, device=DEVICE_INPUT_NUMBER, dtype='int16',
                            channels=1, callback=callback):
            print('#' * 80)
            print('Press Ctrl+C to stop listening...')
            print('#' * 80)

            rec = vosk.KaldiRecognizer(model, samplerate)
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    text = rec.Result()
                    text_json = json.loads(text)
                    if(text:= text_json["text"]):
                        print("[!]Success Sentence:", text)
                        DONE_SENTENCE = True
                        PREV_SENTENCE = ""
                else:
                    partial = rec.PartialResult()
                    partial_json = json.loads(partial)
                    if(partial_entry := partial_json.get("partial")):
                        process_entry(partial_entry)
                        DONE_SENTENCE = False
except KeyboardInterrupt:
    print('\nDone')
    sys.exit(0)
except Exception as e:
    sys.exit(type(e).__name__ + ': ' + str(e))