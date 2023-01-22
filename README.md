# voice-assistant
A small voice desktop assistant written on a booring sunday afternoon

## Instructions for usage:

0 - Install Requirements.

1 - Download the spanish (or others) model from https://alphacephei.com/vosk/models (https://alphacephei.com/vosk/models/vosk-model-small-es-0.3.zip)

2 - unzip and put the content in a new folder named "model" in the same folder as the script.

3 - run with "python assistant.py" or "gui.pyw" , select your device and press Enter.

All commands are related in 'commands_<lang>.json' and 'settings_<lang>.json'.

## Features
 - Execute commands with a hotword like google assistant.
 - Reload commands while the assistant is running.
 - Can execute commands with numeric args.
 - Repeat the last command.
 - You can add more commands and hotwords.


# Command options
    -> run_process : Execute a process
    -> press: A key that will be pressed
        Reference: https://www.autoitscript.com/autoit3/docs/appendix/SendKeys.htm
        ^ Ctrl, # WIN, ! Alt, + or {TAB} for TAB, SHIFT are equal to uppercase letter
    -> ctrl_num :  Press CTRL + NUMBER
    -> alternative:  Synonymous of the command, alternatives to the same sentence
    -> wait(True|False): Wait until the end of the input sentence
    -> voice: Say something when the command is called
    -> {n}: Argument