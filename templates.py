from engine import *


class MainMenu(GameArea):
    def __init__(self, main_object):
        super().__init__()
        resolution = main_object.resolution

        bt_new_game = Button(resolution, 20, 20, 60, 10,
                             border_color=(255, 255, 255), border=2)
        bt_new_game.set_color((150, 150, 150))
        bt_new_game.color_on_mouse_down = pygame.Color('gray')
        bt_new_game.set_text('Начать игру', (0, 0, 0))

        bt_settings = Button(resolution, 20, 40, 60, 10,
                             border_color=(255, 255, 255), border=2)
        bt_settings.set_color((150, 150, 150))
        bt_settings.set_text('Настройки', (0, 0, 0))
        bt_settings.color_on_mouse_down = pygame.Color('gray')
        bt_settings.connect_mouse_up(lambda x: main_object.switch_game_area(main_object.settings))

        bt_exit = Button(resolution, 20, 60, 60, 10,
                         border_color=(255, 255, 255), border=2)
        bt_exit.set_color((150, 150, 150))
        bt_exit.set_text('Выход', (0, 0, 0))
        bt_exit.color_on_mouse_down = pygame.Color('gray')
        bt_exit.connect_mouse_up(main_object.quit)

        self.add_objects(bt_new_game, bt_settings, bt_exit)


class Settings(GameArea):

    def __init__(self, main_object):
        super().__init__()
        resolution = main_object.resolution

        res_condition = lambda obj, key: key.isdigit() and (key != '0' if len(obj.text) == 0 else len(obj.text) < 4)

        te_res_x = TextEdit(resolution, 20, 20, 25, 5, border=2)
        te_res_x.color_default = (200, 200, 200)
        te_res_x.set_color((200, 200, 200))
        te_res_x.color_filling = (160, 160, 160)
        te_res_x.text_condition = res_condition
        te_res_x.set_text(str(resolution[0]))

        te_res_y = TextEdit(resolution, 55, 20, 25, 5, border=2)
        te_res_y.color_default = (200, 200, 200)
        te_res_y.set_color((200, 200, 200))
        te_res_y.color_filling = (160, 160, 160)
        te_res_y.text_condition = res_condition
        te_res_y.set_text(str(resolution[1]))

        lb_res = Object(resolution, 40, 10, 20, 8)
        lb_res.set_text('Разрешение', (255, 255, 255), align='center', valign='center')

        self.add_objects(te_res_x, te_res_y, lb_res)
        # bg = Background(self.resolution, "galaxes\\galaxy_1.jpg")
        # bg.image_mode = '%obj'
        # main_menu.background = bg