import autoit

def run_process(process_name : str):
    def run_process():
        print(f"[+]Runing process {process_name}");\
        autoit.run(f"cmd /c start {process_name}")
    return run_process

def ctrl_num(num : int):
    print(f"[+]Sending CTRL+{num}")
    autoit.send("^"+str(num))

def press_keys(keys : str, repeat : int = 1):
    print(f"[+]Executing hotkeys {keys} {repeat} times.")
    autoit.send(keys*repeat)

def get_win_title():
    return autoit.win_get_title("[ACTIVE]")
