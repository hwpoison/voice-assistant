import tkinter as tk
import tkinter.font as font
from assistant import Assistant 
from tkinter import messagebox
import os, signal

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        ## Create main window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # position bottom right
        self.geometry(f"+{screen_width-400}+{screen_height-100}")

        self.transcription = tk.StringVar()

        self.label_btn = tk.Label(self, 
            textvariable=self.transcription)
        self.label_btn['font'] = font.Font(size=20)
        
        self.after(50, self.update_text)
        self.wm_attributes("-topmost", 1)
        self.update_idletasks()
        ## Run appliction
        self.overrideredirect(1)
        self.label_btn.bind("<B1-Motion>", self.move)
        self.label_btn.bind("<Double-Button-1>", lambda e: self.exit())
        self.label_btn.pack(side=tk.LEFT)
        signal.signal(signal.SIGINT, self.traping)

    def move(self, event):
        x, y = self.winfo_pointerxy()
        self.geometry(f"+{x}+{y}") 

    def update_text(self):
        if not assistant_thread.is_alive():
            self.show_error("Error", "Algo ha fallado.")
            self.exit()
        self.transcription.set(assistant_thread.entry)
        color = "green" if assistant_thread.DONE_COMMAND else "black"
        self.label_btn.configure(fg=color)
        self.after(50, self.update_text)

    def show_error(self, title, message):
        messagebox.showerror(title, message)

    def exit(self):
        confirmation = messagebox.askyesno('Confirmación','¿Cerrar el asistente?')
        if not confirmation: return
        print("[!] Bye...")
        assistant_thread.terminate()
        self.destroy()

    def traping(self, signal, frame):
        exit()
        os.sys.exit(0)


if __name__ == '__main__':
    # initialize assistant thread
    assistant_thread = Assistant()
    assistant_thread.INPUT_DEVICE_INDEX = 1
    assistant_thread.daemon = True # set daemon
    assistant_thread.start()

    # initialize gui
    gui = GUI()
    gui.mainloop()
