from engine import *
import random
import glob
from core import SpaceMap, Planet


class MainMenu(GameArea):
    def __init__(self, main_object):
        super().__init__()
        resolution = main_object.resolution

        bt_new_game = Button(resolution, 20, 20, 60, 10,
                             border_color=(255, 255, 255), border=2)
        bt_new_game.set_color((150, 150, 150))
        bt_new_game.color_on_mouse_down = pygame.Color('gray')
        bt_new_game.set_text('Начать игру', (0, 0, 0))
        bt_new_game.connect_mouse_up(lambda x: main_object.new_game())

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

        bt_down_color = pygame.Color('red')

        bt_ok = Button(resolution, 60, 40, 20, 5, border=2)
        bt_ok.set_color((200, 200, 200))
        bt_ok.color_on_mouse_down = bt_down_color

        def change_res(obj: Button, load_obj):
            main_object.switch_resolution(int(te_res_x.text), int(te_res_y.text), bt_fullscreen.image_enabled)
            main_object.switch_game_area(load_obj)

        bt_ok.connect_mouse_up(lambda e: change_res(e, main_object.main_menu))
        bt_ok.set_text('OK')

        bt_cancel = Button(resolution, 40, 40, 20, 5, border=2)
        bt_cancel.set_color((200, 200, 200))
        bt_cancel.color_on_mouse_down = bt_down_color
        bt_cancel.connect_mouse_up(lambda e: main_object.switch_game_area(main_object.main_menu))
        bt_cancel.set_text('Отмена')

        bt_apply = Button(resolution, 20, 40, 20, 5, border=2)
        bt_apply.set_text('Применить')
        bt_apply.set_color((200, 200, 200))
        bt_apply.color_on_mouse_down = bt_down_color
        bt_apply.connect_mouse_up(lambda e: change_res(e, main_object.settings))

        bt_fullscreen = Button(resolution, 20, 30, 5, 5, adopt_order=0, border_color=(150, 150, 150), border=2)
        bt_fullscreen.set_image('staff\\check_box.jpg', size_mode='%obj')
        bt_fullscreen.image_enabled = main_object.full_screen
        bt_fullscreen.set_color((255, 255, 255))

        def switch_image(e):
            e.image_enabled = not e.image_enabled

        bt_fullscreen.connect_mouse_up(switch_image)
        # bt_fullscreen.image_enabled = False

        lb_fullscreen = Object(resolution, 25, 30, 10, 5)
        lb_fullscreen.set_text('Полный экран', (255, 255, 255), align='left')

        self.add_objects(te_res_x, te_res_y, lb_res, bt_ok, bt_cancel, bt_apply, bt_fullscreen, lb_fullscreen)
        # bg = Background(self.resolution, "galaxes\\galaxy_1.jpg")
        # bg.image_mode = '%obj'
        # main_menu.background = bg


class SpaceMapScreen(GameArea):

    def __init__(self, main_object):
        super().__init__()
        resolution = main_object.resolution
        self.background = Background(resolution, random.choice(glob.glob('galaxes\\*')))
        self.main = main_object

    class APlanet(RadialObject):

        def __init__(self, resolution, planet: Planet, img_number, cls):
            # todo write ships
            y = planet.y_rel + planet.r_rel if planet.y_rel < 50 else planet.y_rel - len(planet.fractions_impact) * 2
            self.stat_boxes = [Object(resolution,
                                      planet.x_rel,
                                      y + i,
                                      5,
                                      2) for i in range(
                0,
                len(planet.fractions_impact) * 2,
                2
            )]
            self.squads = {planet.squads[i]: MovableObject(
                resolution,
                planet.x_rel,
                planet.y_rel,
                2,
                2,
                border=2,
                border_color=(255, 255, 255)
            ) for i in range(len(planet.squads))}
            self.squads = {}
            self.cls = cls
            self.planet = planet
            super().__init__(resolution,
                             planet.x_rel,
                             planet.y_rel,
                             planet.r_rel)
            size = random.randint(3, 8)
            self.img = f'planets\\{img_number}'
            self.img_hd = f'planets_high\\{img_number}'
            self.set_image(self.img, size_mode='%obj')
            self.set_text(planet.name, (0, 255, 0), align='left', text_pos='left' if self.x_rel > 50 else 'right')
            self.set_font(font_scale=40)
            self.stat = False
            for squad in self.squads.values():
                squad.set_color((255, 255, 255))
            for box in self.stat_boxes:
                box.set_text(text_color=(255, 255, 255), align='left')

        def update(self, planet, res):
            self.planet = planet
            for squad in set(self.squads.keys()) - set(planet.squads):
                del self.squads[squad]
            for squad in set(planet.squads) - set(self.squads.keys()):
                self.squads[squad] = MovableObject(
                    res,
                    planet.x_rel,
                    planet.y_rel,
                    2,
                    2,
                    border=2,
                    border_color=(255, 255, 255)
                )
            if planet.status == 'BATTLE':
                self.set_text('!' + self.text)
            elif '!' == self.text[0]:
                self.set_text(self.text[1:])

        def draw(self, screen):
            super().draw(screen)
            if self.stat:
                for box in self.stat_boxes:
                    box.draw(screen)
            for squad in self.squads.values():
                squad.draw(screen)

        def adopt(self, resolution: Tuple[int, int]):
            super().adopt(resolution)
            for box in self.stat_boxes:
                box.adopt(resolution)
            for squad in self.squads.values():
                squad.adopt(resolution)

        def on_hover(self, e, x, y):
            if not self._hovered:
                statistic = sorted(self.planet.get_statistic().items(), key=lambda x: x[0].name)
                for i, item in enumerate(statistic):
                    fract, percent = item
                    self.stat_boxes[i].set_text(f'{fract.name} - {round(percent * 100)}')
            self.stat = True

        def not_hover(self, e, x, y):
            self.stat = False

        def hover(self, x, y):
            super().hover(x, y)
            for squad in self.squads.values():
                squad.hover(x, y)

        def on_mouse_up(self, x, y):
            for squad_game, squad in self.squads.items():
                if self.planet.status == 'BATTLE':
                    self.cls.main.switch_game_area(self.cls.main.battle_screen, self.cls.main.game.space_map.planets.index(self.planet))
                else:
                    if squad.grabbed:
                        for obj in self.cls.objects:
                            if self is not obj and obj.check(squad.x, squad.y):
                                print(squad_game.start_travel(obj.planet))
                    squad.x, squad.y = squad.sx, squad.sy
                squad.on_mouse_up(x, y)

        def on_mouse_down(self, x, y):
            for squad in self.squads.values():
                squad.on_mouse_down(x, y)

    def update(self, main):
        for i, planet in enumerate(self.objects):
            planet.update(main.game.space_map.planets[i], main.resolution)

    def load(self, resolution, space_map: SpaceMap):

        images = random.choices(glob.glob('planets_high\\*.png'), k=len(space_map.planets))
        for i, planet in enumerate(space_map.planets):
            self.add_objects(self.APlanet(resolution, planet, images[i][12:], self))
        super().load(resolution)


class BattleScreen(GameArea):

    def __init__(self, main_object):
        super().__init__()
        self.background = Background(main_object.resolution, 'staff\\space.jpg')
        self.planet_index = None

    def load(self, resolution, planet_index):
        self.planet_index = planet_index

    def update(self, main):
        self.main = main
        self.objects = []
        battle = main.game.space_map.planets[self.planet_index].battle
        for x, y in battle.bullets:
            self.add_objects(RadialObject(main.resolution, x, y, 1, 1))
        for ship in battle.ships:
            pass