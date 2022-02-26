from utils import run_process, ctrl_num, get_win_title

# for invoke command 
hotwords = ['alexa', 'por favor', 'comando', 'ahora', 'ok google','ok']

# for repeat the last command without hotword
again_words = ['otra','otra vez', "repetir comando"]

# for reload modules while the assistant is runing
reload_words = ['recargar módulos']

# numbers in natural language
numbers = ['cero', 'uno','dos','tres','cuatro','cinco','seis','siete','ocho','nueve',
            'diez','once','doce','trece','catorce','quince']

# https://www.autoitscript.com/autoit3/docs/appendix/SendKeys.htm
#^ Ctrl, # WIN, ! Alt, + TAB, SHIFT are equal to uppercase letter
# func , press, context 
command_list = {
    "abrir la consola": {'func':run_process('cmd.exe')}, # run simple process
    ("salir", "escapar"):{'press':"{ESC}"}, # many alternatives for the same command
    # browser context
    "abrir nueva pestaña":{'context':'BROWSER', 'press':'^t'},
    "cerrar pestaña":{'press':'^w', 'context':'BROWSER'},
    "reabrir pestaña":{'press':'^T','context':'BROWSER'},
    "recargar página":{  # the command can work only in a specific context or app
                        'press':'{BROWSER_REFRESH}',
                        'context':'BROWSER'
    },
    "ver la pestaña ([0-9])":   {'func':ctrl_num, 'context':'BROWSER'}, # numeric command with custom function
    ("salir de pantalla completa","pantalla completa"):{'context':'BROWSER', 'press':"{f}"},
    # all contexts
    "siguiente escritorio":{'press':'{RIGHT}'},
    "anterior escritorio": {'press':'^#{LEFT}'},
    "minimizar ventanas":{'press':'#m'},
    ("maximizar las ventanas", "maximizar ventanas"):{'press':'!{TAB}'},
    "tomar una captura": {'press':'#{PRINTSCREEN}'} ,
    "pasar página":{'press':'{PGDN}'},
    "subir página":{'press':'{PGUP}'},
    "buscar":{'press':'^f'},
    "abajo":{'press':'{DOWN}'},
    "abajo ([0-9]) veces":{'press':'{DOWN}'},
    "arriba":{'press':'{UP}'},
    "subir volumen en ([0-9])":{'press':'{VOLUME_UP}'},
    "bajar volumen en ([0-9])":{'press':'{VOLUME_DOWN}'},
    "silenciar sonido":{'press':"{VOLUME_MUTE}"},
    "regresar sonido":{'press':"{VOLUME_UP}"},
    "ir arriba":{'press':"{HOME}"},
    "ir abajo":{'press':"{END}"},
    "siguiente canción":{'press':"{MEDIA_NEXT}"},
    "anterior canción":{'press':"{MEDIA_PREV}"},
    ("pausar", "pausar la música", "parar música","detener música"):{'press':"{MEDIA_PLAY_PAUSE}"},
    "pausar el sonido":{'press':"{MEDIA_PLAY_PAUSE}"},
    ("play", "reanudar el sonido","reanudar la música","reanudar el sonido"):{'press':"{MEDIA_PLAY_PAUSE}"},
    "reproducir música":{'press':"{MEDIA_PLAY_PAUSE}"},
    "abrir el correo":{'func':run_process("outlook.exe")},
    "ir hacia atrás":{'press':"{BROWSER_BACK}"},
    "refrescar":{'press':"{F5}"},
    "cerrar ventana":{'press':"!{F4}"},
    "abrir whatsapp":{'func':run_process("https://web.whatsapp.com/")},
    "abrir youtube":{'func':run_process("https://youtube.com")},
    "abrir el traductor":{'func':run_process("https://deepl.com")},
    "abrir el bloc de notas":{'func':run_process("notepad")}
}

context_list = {
    "BROWSER":['Microsoft Edge', 'Google Chrome'],
    "CMD":['python', 'cmd.exe', 'commands.py']
}

if __name__ == '__main__':
    pass