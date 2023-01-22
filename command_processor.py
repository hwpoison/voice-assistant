import re

import utils
from logger import logger
from speechsynth import speech
from settings import Settings, load_settings

"""
    This module allows to process and executes commands from natural language text
"""

LAST_EXECUTED_COMMAND = None
WAIT_ENTIRE_INPUT = False


def normalize_args(arg):  # normalize arg content according to settings.literals
    if not arg:
        return False

    for nl, lit in Settings.literals.items():
        arg = arg.replace(nl, lit)

    if arg.isdigit():
        return int(arg)

    return arg


def match_command(cmd_list, input_sentence):
    """
        Try to match keyword in a cmd_list
    """
    found_cmd, arg = '', None
    for cmd in cmd_list:
        # if is and exactly match
        if cmd == input_sentence:
            return cmd, None

        # else try match command includes with args (ex: run the {n} program)
        match = re.findall(f"^{ cmd.replace('{n}', '(.+)') }$", input_sentence)
        if match and len(cmd) > len(found_cmd):
            found_cmd = cmd
            arg = match[0]

    return found_cmd, arg


def find_match_command(sentence):
    """
        Iterate over command list and find the best match
    """
    for cmd_key, value in Settings.all_commands.items():
        cmd_list = [cmd_key]
        if synms := value.get('alternative'):  # synonyms availables
            if type(synms) is list:
                cmd_list.extend(synms)
            else:
                logger.warning(f"Alternatives for '{cmd_key}' is not a list!")

        matched_cmd, extracted_arg = match_command(cmd_list, sentence)
        if matched_cmd:
            value['args'] = normalize_args(extracted_arg)
            return value

    return False


def list_to_or_regx_pattern(words_list: list):
    """
    Return a word list to OR style list
        ex:     # ['ok google', 'ahora'] -> (ok google|ahora.+) 
    """
    return f"({'|'.join([w for w in words_list])}*)"


def find_into_str(string: str, word_list: list):
    return re.findall(f"{ list_to_or_regx_pattern(word_list)}\s(.+)", string)


def match_and_filter_hotword(string: str):
    """ 
        Detect and filter match hotword into a sentence
        also OR regex allow to use hotowords with more thatn one word
    """
    hotword = find_into_str(string, Settings.hotwords)
    return False if not hotword else hotword[0][1]


def reload_commands_module():
    logger.info("Reloading settings")
    load_settings()
    logger.info("Settings reloaded")


def get_context():  # check context based on win title
    win_title = utils.get_win_title()
    logger.info(f"Actual window title { win_title }")
    for context, apps in Settings.context_list.items():
        if win_title.endswith(tuple(apps)):
            return context
    return 'UNKNOW'


def intent(entry, check_hotword=True) -> bool:
    """
        Check word and try match a command

    """
    global LAST_EXECUTED_COMMAND, WAIT_ENTIRE_INPUT

    command = entry.strip()

    # check and filter hotword
    if check_hotword:
        filter_sentence = match_and_filter_hotword(command)
        if not filter_sentence:
            return False
        command = filter_sentence
        logger.info("Hotword detected")

    # special reload words
    if command in Settings.reload_words:
        logger.info("Reloading 'settings' module.")
        reload_commands_module()
        return True

    # find command
    cmd_info = find_match_command(command)
    if not cmd_info:
        logger.warning(f"Command '{command}' not found")
        return False
    logger.info(f"Command {command} found - content: {cmd_info}")

    # set lazy status (wait a resolutive input, for ex when the user is writting something)
    if cmd_info.get('wait'):
        WAIT_ENTIRE_INPUT = True
    else:
        WAIT_ENTIRE_INPUT = False

    # check context
    if cmd_context := cmd_info.get('context'):
        actual_context = get_context()
        if actual_context != cmd_context:
            logger.error(f"Wrong context: { cmd_context }")
            logger.error(f"    Actual is: { actual_context }")
            return False

    # supported functions
    functions = {
        'run_process': utils.run_process,
        'press': utils.press_keys,
        'ctrl_num': utils.ctrl_num
    }

    for function_name, function in functions.items():
        if to_execute := cmd_info.get(function_name):
            # check args
            if arg_value := cmd_info.get("args"):
                # arg is present into instance
                if to_execute == '{}':
                    function(arg_value)
                # arg is extract from dict
                else:
                    function(to_execute, arg_value)
            else:
                # if the function has a value ({ run_process: 'chrome.exe' })
                function(to_execute)

    LAST_EXECUTED_COMMAND = entry

    if to_speech := cmd_info.get('voice'):
        speech(to_speech)

    return True


def repeat_last_command():
    logger.info(f"Repeating last command { LAST_EXECUTED_COMMAND }")
    return intent(LAST_EXECUTED_COMMAND)


if __name__ == '__main__':
    execute = intent("ctrl dos", check_hotword=False)
