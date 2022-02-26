import re
import time
import importlib
import commands
from utils import press_keys, get_win_title

LAST_EXECUTED_COMMAND = None


def or_regx_pattern(words_list: list):
    # ['ok google', 'ahora'] -> (ok google|ahora.+)
    return f"({'|'.join([w for w in words_list])}*)"


def natural_to_int(string: str):  # replace all natural numbers to int
    pattern = or_regx_pattern(commands.numbers)
    sub = re.sub(pattern, lambda m: str(
        commands.numbers.index(re.escape(m.group(0)))), string)
    return sub if sub else string


def find_into_str(string: str, word_list: list):
    return re.findall(f"{or_regx_pattern(word_list)}\s(.+)", string)


def get_int_args(string: str) -> int:
    # la cosa numero cinco -> la cosa numero, cinco
    arg_int = re.findall(f"[a-z].+\s([0-9]+)", string)
    return int(arg_int[0]) if arg_int else 0


def filter_hotword(string: str):
    hotword = find_into_str(string, commands.hotwords)
    return False if not hotword else hotword[0][1]


def reload_commands_module():
    importlib.reload(commands)


def make_comparation(keyword, cmd):
    return cmd == keyword or re.findall(cmd, keyword)


def in_str_or_tuple(keyword, cmd):
    if type(cmd) == str:
        return make_comparation(keyword, cmd)
    else:
        for c in cmd:
            search = make_comparation(keyword, c)
            if search:
                return search


def find_command(keyword):
    cmd_key = list(filter(lambda el: in_str_or_tuple(
        keyword, el), commands.command_list))
    return commands.command_list.get(cmd_key[0]) if cmd_key else None


def get_command_context():  # check context based on win title
    win_title = get_win_title()
    print("[i] Actual window title ", win_title)
    for context, apps in commands.context_list.items():
        if win_title.endswith(tuple(apps)):
            return context
    return 'UNKNOW'


def run_command(entry_command, check_hotword=True) -> bool:
    global LAST_EXECUTED_COMMAND

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

    # normalize
    command = natural_to_int(command)

    # find command
    cmd_info = find_command(command)
    if not cmd_info:
        return False

    # check numeral arg (ex: run the tab five)
    cmd_arg = get_int_args(command)
    print(f"[*] Found '{command}' with arg '{cmd_arg}'")

    # check context
    if cmd_context:= cmd_info.get('context'):
        if get_command_context() != cmd_context:
            print("[x] Wrong context: ", cmd_context)
            return False

    # process
    if to_press:= cmd_info.get('press'):
        if cmd_arg:
            press_keys(to_press, repeat=cmd_arg)
        else:
            press_keys(to_press)
    elif to_execute:= cmd_info.get('func'):
        if cmd_arg:
            to_execute(cmd_arg)  # custom function with arg
        else:
            try:
                to_execute()
            except TypeError:
                print("[x] Error to execute command:", command)
                return False

    LAST_EXECUTED_COMMAND = entry_command
    return True


def repeat_last_command():
    print("[+]Repeating last command ", LAST_EXECUTED_COMMAND)
    return run_command(LAST_EXECUTED_COMMAND)


if __name__ == '__main__':
    n = run_command("abajo cinco veces", False)
    print(n)
