import autoit
import sys
from logger import logger


def run_process(process_name: str):
    logger.info(f"Runing process '{process_name}'")
    autoit.run(f"cmd /c start {process_name}")


def ctrl_num(num: int):
    logger.info(f"Sending CTRL+{num}")
    autoit.send("^"+str(num))


def press_keys(keys: str, repeat: int = 1):
    logger.info(f"Executing hotkeys '{keys}' {repeat} times.")
    autoit.send(keys*repeat)


def get_win_title():
    return autoit.win_get_title("[ACTIVE]")


def press_write(text: str):
    logger.info(f"Writing the text '{text}'")
    return autoit.send(str(text))


def close_assistant():
    sys.exit(0)
