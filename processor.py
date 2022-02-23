import re
import time
import importlib
import commands
from utils import press_keys, get_win_title

LAST_EXECUTED_COMMAND = None

def or_regx_pattern(words_list : list):
    # ['ok google', 'ahora'] -> (ok google|ahora.+)
    return "|".join([n for n in list(map(lambda c: str(c), words_list))])

def nlnumber_to_int(num : str): # returns natural language number to integer
    return commands.numbers.index(num) if num in commands.numbers else False

def find_into_str(string : str, word_list : list):
    return re.findall(f"({or_regx_pattern(word_list)})\s(.+)", string)

def get_int_args(string : str):
    # la cosa numero cinco -> la cosa numero, cinco
    return re.findall(f"([a-z].+)\s({ or_regx_pattern(commands.numbers)}.+)", string)

def filter_hotword(string : str):
    hotword = find_into_str(string, commands.hotwords)
    return False if not hotword else hotword[0][1]
    
def reload_commands_module():
    importlib.reload(commands)
    
def in_str_or_tuple(keyword, key):
    if type(key) == str:
        return key == keyword
    else:
        return keyword in key
        
def find_command(key_):
    cmd_key = list(filter(lambda el: in_str_or_tuple(key_, el), commands.command_list))
    return commands.command_list.get(cmd_key[0]) if cmd_key else None 

def get_command_context(): # check context based on win title
    win_title = get_win_title()
    print("[i] Actual window title ", win_title)
    for context, apps in commands.context_list.items():
        if win_title.endswith(tuple(apps)):
            return context 
    return 'UNKNOW'

def run_command(entry_command, check_hotword=True) -> bool:
    global LAST_EXECUTED_COMMAND
    
    command = entry_command.strip()
    arg_number = None
    
    # check and filter hotword
    if check_hotword:
        command = filter_hotword(command)
        if not command:
            return False
            
    # special reload words
    if command in commands.reload_words: 
        print("[*] Reloading 'commands' module.")
        reload_commands_module()
        return True 
    
    # cmd with int arg (ex: run the tab five)
    if argv := get_int_args(command):
        argv = argv[0]
        command = argv[0].strip()   
        arg_number = nlnumber_to_int(argv[1].strip())
        print(f"[*] Executing '{command}' with arg '{arg_number}'")
    
    # find command
    cmd_info = find_command(command)
    if not cmd_info:
        return False
    
    # check context 
    if cmd_context := cmd_info.get('context'):
        if get_command_context() != cmd_context:
            print("[x] Wrong context: ", cmd_context)
            return False
            
    # process 
    if to_press := cmd_info.get('press'):
        if arg_number:
            press_keys(to_press, repeat=arg_number)
        else:
            press_keys(to_press)
    elif to_execute := cmd_info.get('func'):
        if arg_number: 
            to_execute(arg_number) # custom function with arg
        else:
            try:to_execute()
            except TypeError:
                print("[x] Error to execute command:", command)
                return False
                
    LAST_EXECUTED_COMMAND = entry_command
    return True

def repeat_last_command():
    print("[+]Repeating last command ", LAST_EXECUTED_COMMAND)
    run_command(LAST_EXECUTED_COMMAND)

if __name__ == '__main__':
    #import time
    #time.sleep(3)
    n = run_command("ahora subir volumen en")
    print(n)