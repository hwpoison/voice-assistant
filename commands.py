from utils import run_process, ctrl_num

# for invoke command 
hotwords = ['por favor', 'comando', 'ahora', 'ok google','ok']

# for repeat the last command without hotword
again_words = ['otra','otra vez']

# for reload modules
reload_words = ['recargar módulos']

# nl numbers
numbers = ['cero', 'uno','dos','tres','cuatro','cinco','seis','siete','ocho','nueve',
            'diez','once','doce','trece','catorce','quince']


# https://www.autoitscript.com/autoit3/docs/appendix/SendKeys.htm
#^ Ctrl, # WIN, ! Alt, + TAB, SHIFT are equal to uppercase letter
action_list = {
    "abrir la consola":run_process('cmd.exe'),
    "ver la pestaña":ctrl_num, # numeric command with custom function
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
    "subir volumen en":"{VOLUME_UP}", # numeric command
    "bajar volumen en":"{VOLUME_DOWN}",
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
    "abrir whatsapp":run_process("https://web.whatsapp.com/"),
    "abrir youtube":run_process("https://youtube.com"),
    "abrir el traductor":run_process("https://deepl.com"),
    "abrir bloc de notas":run_process("notepad")
}