import os
import queue
import sys
import json
from threading import Thread, Event

import sounddevice as sd
import vosk
import command_processor 
import commands

class Assistant(Thread):
    def __init__(self):
        super().__init__()
        self.audio_blocks_queue = queue.Queue()
        self.MODEL_FOLDER = 'model'
        self.entry = ' '
        self.stream = None
        self.event = None
        self.DONE_COMMAND = False # check success cmd
        self.PREVIOUS_ENTRY = None # prevents repeat
        self.INPUT_DEVICE_INDEX = None
        self.BLOCK_SIZE = 8000

    def select_device(self):
        print('Available inputs devices, please select your input device (choice with '>' symbol):')
        print(sd.query_devices())
        self.INPUT_DEVICE_INDEX = int(input("[INPUT DEVICE NUMBER]:"))

    def analize_entry(self, entry):
        if entry and self.PREVIOUS_ENTRY != entry:
            print(f'[i] Analyzing entry "{entry}"')
            if entry in commands.again_words:
                cmd = command_processor.repeat_last_command()
            else:
                cmd = command_processor.run_command(entry)
                self.DONE_COMMAND = cmd if cmd else False
            self.PREVIOUS_ENTRY = entry

    def callback(self, indata, frames, time, status):
        self.audio_blocks_queue.put(bytes(indata))

    def terminate(self):
        if self.stream:
            self.stream.abort()
            self.event.set()
            print("[x] Assistant thread aborted.")
        sys.exit(0)

    def run(self):
        if not self.INPUT_DEVICE_INDEX:
            print("[X] Input device not selected.")
            self.terminate()
        try:
            device_info = sd.query_devices(self.INPUT_DEVICE_INDEX, 'input')
            # soundfile expects an int, sounddevice provides a float:
            samplerate = int(device_info['default_samplerate'])
            model = vosk.Model(self.MODEL_FOLDER)
            self.event = Event()
            with sd.RawInputStream(samplerate=samplerate, blocksize = self.BLOCK_SIZE, 
                            device=self.INPUT_DEVICE_INDEX, dtype='int16',
                            channels=1, callback=self.callback) as self.stream:
                print('#' * 80)
                print('Ready, press Ctrl+C to stop listening...')
                print('#' * 80)
                rec = vosk.KaldiRecognizer(model, samplerate)
                while True:
                    data = self.audio_blocks_queue.get() # get audio block from queue
                    if rec.AcceptWaveform(data): # final sentence
                        text = rec.Result()
                        text_json = json.loads(text)
                        if(full_entry:= text_json["text"]):
                            # Reset previous sentence
                            self.PREVIOUS_ENTRY = "" 
                            if not self.DONE_COMMAND:
                                # process total and corrected input sentence
                                # if partial result is not conclusive
                                print('[i] Analyzing entire entry')
                                self.analize_entry(full_entry)
                                self.entry = full_entry
                                #self.entry = ""
                            # Reset model TODO: fix memory leak ( .Reset() method apparently not working )
                            rec = vosk.KaldiRecognizer(model, samplerate) 
                    else:
                        partial = rec.PartialResult() # partial sentence
                        partial_json = json.loads(partial)
                        if(partial_entry := partial_json.get('partial')):
                            #print("[!]Partial entry:", partial_entry)
                            # process partial input
                            self.analize_entry(partial_entry)
                            self.entry = partial_entry
                self.event.wait()

        except KeyboardInterrupt:
            print('\n[i] Done')
            self.terminate()
            sys.exit(0)
        except Exception as e:
            self.terminate()
            sys.exit(type(e).__name__ + ': ' + str(e))

if __name__ == '__main__':
    assistant_th = Assistant()
    assistant_th.select_device()
    assistant_th.run()
    input()