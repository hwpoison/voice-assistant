import json
from logger import logger
from dataclasses import dataclass


@dataclass
class Settings:
    lang: str # IETF language tag (en, es, ..) https://en.wikipedia.org/wiki/IETF_language_tag
    voice : bool
    auto_select_device: bool

@dataclass
class Intents:
    hotwords: dict
    welcome_messages: dict
    again_words: dict
    reload_words: dict
    context_list: dict
    numbers: dict
    literals: dict
    all_commands: dict


Intents.all_commands = {}


def save_intents():
    logger.info("Saving intents")

    intents = {
        'commands': Intents.all_commands,
        'hotwords': {
            'activation': Intents.hotwords,
            'again': Intents.again_words,
            'reload': Intents.reload_words
        },
        'welcome_messages': Intents.welcome_messages,
        'context_list': Intents.context_list,
        'numbers': Intents.numbers,
        'literals': Intents.literals

    }

    with open(f'configurations/intents_{Settings.lang}.json', 'w', encoding="utf-8") as fp:
        fp.write(json.dumps(intents, ensure_ascii=False, indent=4))


def save_settings():
    settings = {
        'lang': Settings.lang,
        'voice': Settings.voice,
        'auto_select_device': Settings.auto_select_device
    }
    with open(f'configurations/settings.json', 'w', encoding='utf-8') as fp:
        fp.write(json.dumps(settings, ensure_ascii=False, indent=4))


def load_intents():
    logger.info(f"Loading { Settings.lang } intents file")
    with open(f'configurations/intents_{Settings.lang}.json', 'r', encoding='utf-8') as fp:
        loaded_intents = json.loads(fp.read())

    Intents.all_commands = loaded_intents['commands']
    Intents.hotwords = loaded_intents['hotwords']['activation']
    Intents.again_words = loaded_intents['hotwords']['again']
    Intents.reload_words = loaded_intents['hotwords']['reload']
    Intents.welcome_messages = loaded_intents['welcome_messages']
    Intents.context_list = loaded_intents['context_list']
    Intents.numbers = loaded_intents["numbers"]
    loaded_intents['literals'].update({loaded_intents['numbers'][inum]: str(
        inum) for inum in range(0, len(loaded_intents['numbers']))})
    Intents.literals = loaded_intents['literals']


def load_settings():
    logger.info("Loading settings file")
    with open(f'configurations/settings.json', 'r', encoding='utf-8') as fp:
        loaded_settings = json.loads(fp.read())
    Settings.lang = loaded_settings['lang']
    Settings.voice = loaded_settings['voice']
    Settings.auto_select_device = loaded_settings['auto_select_device']

if __name__ == "__main__":
    pass
else:
    load_settings()
    load_intents()