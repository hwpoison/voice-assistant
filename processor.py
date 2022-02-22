import re
import time
import importlib
import commands
from utils import press_keys

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
    print("[*]Reloading 'commands' module.")
    importlib.reload(commands)


def in_str_or_tuple(keyword, key):
    if type(key) == str:
        return key == keyword
    else:
        return keyword in key
        
def find_command(key_):
    cmd_key = list(filter(lambda el: in_str_or_tuple(key_, el), commands.command_list))
    return commands.command_list.get(cmd_key[0]) if cmd_key else None 

def run_command(command, check_hotword=True) -> bool:
    global LAST_EXECUTED_COMMAND
    
    # check and filter hotword
    if check_hotword:
        command = filter_hotword(command)
        if not command:
            return False
            
    # special reload words
    if command in commands.reload_words: 
        reload_commands_module()
        return True 
  
    # cmd with int arg (ex: run the tab five)
    if argv := get_int_args(command):
       argv = argv[0]
       print(f"[*]Executing {command} (Arg type)")
       command = argv[0].strip()
       argument = nlnumber_to_int(argv[1].strip())
       if to_execute := find_command(command):
          if type(to_execute) == str:
            press_keys(to_execute, repeat=argument)
          else:
            to_execute(argument) # custom function with arg
    # simple cmd (ex: mute sound)
    elif to_execute := find_command(command):
        print(f"[*]Executing {command}")
        if type(to_execute) == str:
            press_keys(to_execute)
        else:
            try:
                to_execute() # custom function
            except TypeError:
                return False # without valid argument
                
    LAST_EXECUTED_COMMAND = command
    return True

def repeat_last_command():
    print("[+]Repeating last command ", LAST_EXECUTED_COMMAND)
    run_command(LAST_EXECUTED_COMMAND, check_hotword=False)


if __name__ == '__main__':
    pass