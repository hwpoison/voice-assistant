import json
from logger import logger
from dataclasses import dataclass

@dataclass
class Settings:
    lang : str
    hotwords : dict
    welcome_messages : dict
    again_words : dict
    reload_words : dict
    context_list : dict
    numbers : dict
    literals : dict
    all_commands : dict 

Settings.lang = "es"
Settings.all_commands = {}

def save_settings():
    # settings.json
    with open(f'configurations/settings_{Settings.lang}.json', 'w', encoding='utf-8') as fp:
        fp.write(json.dumps(Settings.all_settings, ensure_ascii=False, indent=4))

    # commands_lang.json
    with open(f'configurations/commands_{Settings.lang}.json', 'w', encoding="utf-8") as fp:
        fp.write(json.dumps(Settings.all_commands, ensure_ascii=False, indent=4))

def load_settings():
    with open(f'configurations/settings_{Settings.lang}.json', 'r', encoding='utf-8') as fp:
        loaded_settings = json.loads(fp.read())

    with open(f'configurations/commands_{Settings.lang}.json', 'r', encoding='utf-8') as fp:
        loaded_commands = json.loads(fp.read())
        Settings.all_commands = loaded_commands
    
    Settings.hotwords = loaded_settings['hotwords']
    Settings. welcome_messages = loaded_settings['welcome_message']
    Settings.again_words = loaded_settings['again_words']
    Settings.reload_words = loaded_settings['reload_words']
    Settings.context_list = loaded_settings['context_list']
    Settings.numbers = loaded_settings["numbers"]
    loaded_settings['literals'].update({loaded_settings['numbers'][inum]: str(
        inum) for inum in range(0, len(loaded_settings['numbers']))})
    Settings.literals = loaded_settings['literals']

load_settings()