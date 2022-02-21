#!/usr/bin/env python3
import os
import queue
import sounddevice as sd
import vosk
import sys
import json 
import importlib 
import hotwords 

q = queue.Queue()

print("Available inputs devices, please select your input device (choice with '>' symbol):")
print(sd.query_devices())
DEVICE_INPUT_NUMBER = int(input("[INPUT DEVICE NUMBER]:"))


def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


def reload_hotwords():
    importlib.reload(hotwords)

DONE_SENTENCE = False
PREV_SENTENCE = ""
PREV_SENTENCE_EXEC_CMD = ""

def detect_hotword(entry):
    global PREV_SENTENCE, PREV_SENTENCE_EXEC_CMD
    # repeat last command
    if entry in hotwords.again_words:
        if DONE_SENTENCE:
            print("[+]Repeating command ", PREV_SENTENCE_EXEC_CMD)
            hotwords.run(PREV_SENTENCE_EXEC_CMD)
    
    if entry in hotwords.reload_words:
        if PREV_SENTENCE != entry:
            print("[!]Reloading 'hotwords' module")
            importlib.reload(hotwords)
            PREV_SENTENCE = entry
            
    # process new command
    entry = hotwords.detect_hotword(entry)
    if entry: # detect hotwor
        command = entry[0][1]
        if PREV_SENTENCE != command:
            print(f"[*]Executing {command}")
            exec = hotwords.run(command)
            if exec:
                PREV_SENTENCE_EXEC_CMD =  command
            PREV_SENTENCE = command

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
                    if(chunk := partial_json.get("partial")):
                        detect_hotword(chunk)
                        DONE_SENTENCE = False
               #if dump_fn is not None:
               #    dump_fn.write(data)

except KeyboardInterrupt:
    print('\nDone')
    sys.exit(0)
except Exception as e:
    sys.exit(type(e).__name__ + ': ' + str(e))