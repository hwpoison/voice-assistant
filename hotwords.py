import re
import autoit
import time

hotwords = ['por favor', 'comando', 'ahora', 'ok google']
again_words = ['otra','otra vez']
reload_words = ['recargar módulos']
#primitives   

def run_program(name):
    print(f"[+]Executing {name}")
    autoit.send("#r")
    time.sleep(0.5)
    autoit.send(name)
    autoit.send("{ENTER}")

def run_process(process_name):
    print(f"[+]Runing process {process_name}")
    autoit.run(f"cmd /c start {process_name}")
    
def ctrl_num(num : int):
    print(f"[+]Sending CTRL+{num}")
    autoit.send("^"+str(num))

def exc_hotkey(keys : str):
    print(f"[+]Executing hotkeys {keys}")
    autoit.send(keys)
    
def or_regx_pattern(words_list):
    # ['ok google', 'ahora'] -> (ok google|ahora.+)
    return "|".join([n for n in list(map(lambda c: str(c), words_list))])

def vol_up(num : int):
    autoit.send("{VOLUME_UP}"*num)
    
def vol_down(num : int):
    autoit.send("{VOLUME_DOWN}"*num)

# nl numbers
numbers = {
   'uno':1,'dos':2,'tres':3,'cuatro':4,'cinco':5,
   'seis':6, 'siete':7, 'ocho':8, 'nueve':9, 'diez':10,
   'once':11, 'doce':12,'trece':13,'catorce':14,'quince':15
}

def find_into_str(string, word_list):
    return re.findall(f"({or_regx_pattern(word_list)})\s(.+)", string)

def get_int_args(string):
    # la cosa numero cinco -> la cosa numero, cinco
    return re.findall(f"([a-z].+)({ or_regx_pattern(numbers)}.+)", string)

def detect_hotword(string, hotwords=hotwords):
    return find_into_str(string, hotwords)


# https://www.autoitscript.com/autoit3/docs/appendix/SendKeys.htm
#^ Ctrl, # WIN, ! Alt, + TAB, SHIFT are equal to uppercase letter
action_list = {
    "abrir la consola":{
        'type':'run_func', 
        'func':lambda: run_program('cmd.exe')
    },
    "ver la pestaña":{
        'type':'int_arg_func',
        'func':ctrl_num
    },
    "abrir bloc de notas":{
        'type':'run_func', 
        'func':lambda: run_process("notepad")
    },
    "siguiente escritorio":"^#{RIGHT}",
    "anterior escritorio":"^#{LEFT}",
    "minimizar ventanas":"#m",
    "maximizar ventanas":"!{TAB}",
    "tomar una captura":"#{PRINTSCREEN}",
    "pasar página":"{PGDN}",
    "subir página":"{PGUP}",
    "buscar":"^f",
    "abrir nueva pestaña":"^t",
    "cerrar pestaña":"^w",
    "reabrir pestaña":"^T",
    "abajo":"{DOWN}",
    "arriba":"{UP}",
    "subir volumen en":{"type":"int_arg_func", "func":vol_up},
    "bajar volumen en":{"type":"int_arg_func", "func":vol_down},
    "silenciar sonido":"{VOLUME_MUTE}",
    "regresar sonido":"{VOLUME_MUTE}",
    "siguiente canción":"{MEDIA_NEXT}",
    "anterior canción":"{MEDIA_PREV}",
    "parar música":"{MEDIA_PLAY_PAUSE}",
    "pausar el sonido":"{MEDIA_PLAY_PAUSE}",
    "reanudar el sonido":"{MEDIA_PLAY_PAUSE}",
    "reproducir música":"{MEDIA_PLAY_PAUSE}",
    "abrir el correo":"{LAUNCH_MAIL}",
    "ir hacia atrás":"{BROWSER_BACK}",
    "recargar":"{F5}",
    "recargar página":"{BROWSER_REFRESH}",
    "cerrar ventana":"!{F4}",
    "escapar":"{ESC}",
    "abrir whatsapp":{"type":"exc_func", "func": lambda: run_process("https://web.whatsapp.com/")},
    "abrir youtube":{"type":"exc_func", "func": lambda: run_process("https://youtube.com")},
    "abrir el traductor":{"type":"exc_func", "func": lambda: run_process("https://deepl.com")}
}


def run(cmd):
    # cmd with int arg (ex: run the tab five)
    if argv := get_int_args(cmd):
       argv = argv[0]
       print("[+]Executing command with int arg.")
       line = argv[0].strip()
       if action := action_list.get(line):
          action['func'](numbers[argv[1]])
          
    elif cmd in action_list:
        cmd_let = action_list[cmd]
        if type(cmd_let) == dict and cmd_let['type'] == 'int_arg_func':
            return False
        if ((type(cmd_let) == dict)
            and (func := cmd_let.get('func'))):
               func() 
        else:
            # simple hotkey 
            exc_hotkey(cmd_let)
    else:
        return False
    return True

if __name__ == '__main__':
    pass