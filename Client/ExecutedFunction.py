import keyboard
from ClientMain import *


def functionToExecute() -> None:
    """
    Method to be executed upon run of the program
    :return: None
    """
    # using keyboard to control the drone. Can be changed
    keyboard.add_hotkey('w', forward, timeout=0)
    keyboard.add_hotkey('s', back, timeout=0)
    keyboard.add_hotkey('a', left, timeout=0)
    keyboard.add_hotkey('d', right, timeout=0)
    keyboard.add_hotkey('e', turnRight, timeout=0)
    keyboard.add_hotkey('q', turnLeft, timeout=0)
    keyboard.add_hotkey('page up', up, timeout=0)
    keyboard.add_hotkey('page down', down, timeout=0)
    keyboard.add_hotkey('space', hover, timeout=0)
    keyboard.add_hotkey('esc', finishExecution, timeout=0)  # Quitting the program when pressed

    # goto(x=-5.5, y=-5.9, z=-1.1, velocity=5.4, hasToFinish=True)
    # goto function is available but not bound to key
