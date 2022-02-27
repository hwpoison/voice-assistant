import re
import time
import importlib
import commands
from utils import press_keys, get_win_title
from speechsynth import speech

"""
    This module allows to process and executes commands from natural language text
"""

LAST_EXECUTED_COMMAND = None
LAZY_MODE = False 

def or_regx_pattern(words_list: list):
    # ['ok google', 'ahora'] -> (ok google|ahora.+)
    return f"({'|'.join([w for w in words_list])}*)"

def parse_arg(arg): # normalize arg content
    if not arg: return False
    for nl, lit in commands.literals.items():
        arg = arg.replace(nl, lit)
    if arg.isdigit():
        return int(arg)
    return arg

def parse_cmd(cmd): # normalize command
    cmd = cmd.replace('{n}', '(.+)')
    return cmd
    
def compare_key(cmd_key, keyword): # return command key and extract args
    found_cmd, arg = "", None
    if type(cmd_key) is not tuple: 
        cmd_key = tuple([cmd_key])
    for subcmd in cmd_key:
       if subcmd == keyword:
            return subcmd, None
       search = re.findall(f"^{ parse_cmd(subcmd) }$", keyword)
       if search and len(subcmd) > len(found_cmd): # choice the more longest
            found_cmd = subcmd
            arg = search[0]
    return found_cmd, arg
     
def find_get_command(sentence): # search and get command values
    for cmd_key, value in commands.command_list.items():
        cmd, arg = compare_key(cmd_key, sentence)
        if cmd:
            value['args'] = parse_arg(arg)
            return value
    return False    
    
def find_into_str(string : str, word_list : list):
    return re.findall(f"{or_regx_pattern(word_list)}\s(.+)", string)

def filter_hotword(string: str):
    hotword = find_into_str(string, commands.hotwords)
    return False if not hotword else hotword[0][1]

def reload_commands_module():
    importlib.reload(commands)

def get_command_context():  # check context based on win title
    win_title = get_win_title()
    print("[i] Actual window title ", win_title)
    for context, apps in commands.context_list.items():
        if win_title.endswith(tuple(apps)):
            return context
    return 'UNKNOW'

def run_command(entry_command, check_hotword=True) -> bool:
    global LAST_EXECUTED_COMMAND, LAZY_MODE

    command = entry_command.strip()

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

    # find command
    cmd_info = find_get_command(command)
    if not cmd_info:
        return False
    
    # set lazy status 
    if cmd_info.get('lazy'):
        LAZY_MODE = True 
    else: 
        LAZY_MODE = False
    
    # check context
    if cmd_context:= cmd_info.get('context'):
        actual_context = get_command_context()
        if actual_context != cmd_context:
            print("[x] Wrong context: ", cmd_context)
            print("    Actual is:", actual_context)
            return False
            
    # process
    if to_press:= cmd_info.get('press'):
        if arg:=cmd_info.get('args'):
            press_keys(to_press, repeat=arg)
        else:
            press_keys(to_press)
    elif to_execute:= cmd_info.get('func'):
        if arg:=cmd_info.get('args'):
            to_execute(arg)  # custom function with arg
        else:
            try:
                to_execute()
            except TypeError:
                print("[x] Error to execute command:", command)
                return False

    LAST_EXECUTED_COMMAND = entry_command
    
    if to_speech:=cmd_info.get('voice'):
        speech(to_speech)
    return True


def repeat_last_command():
    print("[+]Repeating last command ", LAST_EXECUTED_COMMAND)
    return run_command(LAST_EXECUTED_COMMAND)


if __name__ == '__main__':
    pass