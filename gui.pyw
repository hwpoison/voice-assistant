import os
import random
import gc
import signal
from threading import Thread
import sounddevice as sd
import tkinter as tk
import tkinter.font as font
from tkinter import messagebox
from speechsynth import speech

from settings import Settings, Intents
from assistant import Assistant
from intents_processor import reload_intents
from logger import logger

class SelectDevice(tk.Tk):
    """ Selection input audio device screen """

    def __init__(self):
        super().__init__()
        self.geometry("600x500")
        self.resizable(0, 0)
        self.columnconfigure(1, weight=30)
        self.title('Configuration')

        tk.Label(self, text="Select input device (double click):").grid(
            pady=5, row=0, column=1)
        self.device_list = tk.Listbox(width=65, height=20)
        self.choice_btn = tk.Button(self, text="Done",
                                    width=30, command=self.select_device)

        # populate listbox
        self.get_input_devices()
        self.device_list.bind('<Double-Button-1>',
                              lambda e: self.select_device())
        self.device_list.configure(
            background="skyblue4", foreground="white", font=('Aerial 13'))

        if default_input := self.get_default_input_device():
            self.device_list.itemconfig(default_input,
                                        {'bg': 'khaki3'})
            self.device_list.select_set(default_input)

        self.device_list.grid(pady=5, row=2, column=1)
        self.choice_btn.grid(padx=0, pady=5, row=3, column=1)
        self.mainloop()

    def get_input_devices(self):
        devices = str(sd.query_devices()).split('\n')
        self.device_list.insert(tk.END, *devices)

    def select_device(self):
        for i in self.device_list.curselection():
            logger.info(f"[+] Selected { self.device_list.get(i) } -> { i }")
            assistant_thread.INPUT_DEVICE_INDEX = i
            break
        self.destroy()

    def get_default_input_device(self):
        default_input_device = list(
            filter(lambda c: c[0] == '>', str(sd.query_devices()).split('\n')))
        if default_input_device:
            return int(default_input_device[0][3])
        return False


class GUI(Thread):
    """ float transcription text """

    def __init__(self):
        # Create main window
        self.root = tk.Tk()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # position bottom right
        self.root.geometry(f"+{screen_width-400}+{screen_height-100}")

        self.transcription = tk.StringVar()

        self.label_btn = tk.Label(self.root,
                                  textvariable=self.transcription)
        self.label_btn['font'] = font.Font(size=20)

        self.root.after(50, self.update_text)
        self.root.wm_attributes("-topmost", 1)  # top screen
        self.root.update_idletasks()
        # Run appliction
        self.root.overrideredirect(1)
        self.label_btn.bind("<B1-Motion>", self.move)
        self.label_btn.bind("<Double-Button-1>",
                            lambda e: self.exit(need_confirm=True))
        self.label_btn.pack(side=tk.LEFT)

        # menu
        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(
            label="Reload Assistant Commands", command=reload_intents)
        self.menu.add_separator()
        self.menu.add_command(
            label="Close", command=lambda: self.exit(need_confirm=True))

        self.label_btn.bind("<Button-3>", self.do_popup)

        signal.signal(signal.SIGINT, self.traping)
        self.root.mainloop()

    def hide_transcription(self):
        self.label_btn.pack_forget()

    def do_popup(self, event):
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def move(self, event):
        x, y = self.root.winfo_pointerxy()
        self.root.geometry(f"+{x}+{y}")

    def update_text(self):
        self.label_btn.pack(side=tk.LEFT)
        if not assistant_thread.is_alive():
            self.show_error("Error", "Something has failed, exiting...")
            self.exit()
        self.transcription.set(assistant_thread.entry[0:27])
        color = "green" if assistant_thread.DONE_COMMAND else "black"
        self.label_btn.configure(fg=color)
        self.root.after(50, self.update_text)

    def show_error(self, title, message):
        messagebox.showerror(title, message)

    def exit(self, need_confirm=False):
        if need_confirm:
            confirmation = messagebox.askyesno(
                'Confirm', 'Close the assistant?')
            if not confirmation:
                return
        logger.info("Assistant closed by user")
        assistant_thread.terminate()
        self.root.destroy()

    def traping(self, signal, frame):
        exit()
        os.sys.exit(0)


if __name__ == '__main__':
    # initialize assistant thread

    assistant_thread = Assistant()
    if not Settings.auto_select_device:
        assistant_thread.INPUT_DEVICE_INDEX = None

    if not assistant_thread.INPUT_DEVICE_INDEX:
        # init device selection window
        SelectDevice()
        # collect gargabed from closed device selection window thread to avoid future
        # gc action that can accidentadlly kill the gui main thread
        gc.collect()

    assistant_thread.daemon = True  # set daemon
    assistant_thread.start()
    if Settings.voice:
        speech(random.choice(Intents.welcome_messages))
    # initialize gui and join main thread
    gui = GUI()
    gui.start()
    gui.join()
