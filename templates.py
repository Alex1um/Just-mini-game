from engine import *


MAIN_MENU = GameArea()
SPACE_MAP = GameArea()

resolution = (1, 1)

bt_start = Button(resolution, 30, 40, 20, 5)
bt_start.connect_mouse_up(lambda: SPACE_MAP.load() and MAIN_MENU.load())
MAIN_MENU.add_objects(bt_start)