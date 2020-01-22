import time
from typing import *
import pygame
from threading import Thread

"""
all cords and sizes are % of resolution by default
"""

DEFAULTFONT = 'Arial'
percent_img = NewType("'%img'", str)
percent_obj = NewType("'%obj", str)
pixels = NewType("px", str)
rgba = NewType('rgba', Tuple[int, int, int, int])
hsva = NewType('hsva', Tuple[int, int, int, int])
rgb = NewType('rgb', Tuple[int, int, int])


def nothing(*args, **kwargs):
    """
    just nothing
    :param args:
    :param kwargs:
    :return:
    """
    pass


class Interface:
    """
    class for interface(same as Game_Area)
    but may be global
    """

    def __init__(self, click: callable, screen):
        self.click_foo = click
        self.screen = screen
        self.buttons = []
        self.sprites = pygame.sprite.Group()


class Sizible:

    def __init__(self, x_rel=0, y_rel=0, w_rel=1, h_rel=1, adopt_size=True, adopt_cords=True,):
        self.x_rel = x_rel
        self.y_rel = y_rel
        self.w_rel = w_rel
        self.h_rel = h_rel
        self.adopt_size = True
        self.adopt_cords = True

    def adopt(self, resolution):
        if self.adopt_size:
            self.w, self.h = self.w_rel * resolution[0] // 100, self.h_rel * \
                             resolution[1] // 100
        if self.adopt_cords:
            self.x, self.y = self.x_rel * resolution[0] // 100, self.y_rel * \
                             resolution[1] // 100

    def resize(self, w_rel=None, h_rel=None, adopt_size=None, resolution=None):
        """
        resize or switch parameter
        :param w_rel: width % of resolution
        :param h_rel: height % of resolution
        :param adopt_size:
        :param resolution:
        :return:
        """
        if adopt_size:
            self.adopt_size = adopt_size
        if w_rel:
            self.w_rel = w_rel
        if h_rel:
            self.h_rel = h_rel
        if resolution:
            self.adopt(resolution)


class Image:
    """
    class for using images
    """

    def __init__(self,
                 file_name: str=None,
                 width=100,
                 height=100,
                 mode: Union[percent_img, percent_obj, pixels]='%img',
                 animated: bool=False,
                 animation_delay_frames: int=0):
        """
        init image
        :param file_name: name of file
        :param width: width % or px
        :param height: height % or px
        :param mode: mode to scale image
        :param animated: is it animation
        :param animation_delay_frames: delay between switching images if animated
        """
        if file_name:
            self._image = [pygame.image.load(file_name)]
        else:
            self._image = []
        self.animation_delay_frames = animation_delay_frames
        self.frame = 0
        self.image_animated = animated
        self.image_index = 0
        self.image_width = width
        self.image_height = height
        self.image_mode = mode

    def add_images(self, *images: str):
        """
        add multiple images
        :param images: file names
        :return:
        """
        for name in images:
            self._image.append(pygame.image.load(name))

    def set_image(self,
                  image_name: str = None,
                  width: int = 100,
                  height: int = 100,
                  size_mode: Union[percent_obj, percent_img, 'pixels'] = '%img',
                  index=0):
        """
        setting image or image params
        :param image_name: name of new image
        :param width:
        :param height:
        :param size_mode: mode for rescale
        :param index: index of image
        :return:
        """
        if image_name:
            if len(self._image) < index:
                self._image[index] = pygame.image.load(image_name)
            else:
                self.add_images(image_name)
        if size_mode:
            self.image_mode = size_mode
        if width:
            self.image_width = width
        if height:
            self.image_height = height

    def image_render(self, w_abs: int=None, h_abs: int=None) -> pygame.SurfaceType:
        """
        render image with current mode
        :param w_abs: width of object to scale image
        :param h_abs: height of object to scale image
        :return: image
        """
        if self.image_animated:
            if self.frame == self.animation_delay_frames:
                self.image_index = (self.image_index + 1) % len(self._image)
                self.frame = 0
            else:
                self.frame += 1
        if self._image:
            if self.image_mode == '%obj':
                return pygame.transform.scale(self._image[self.image_index],
                                                    (w_abs * self.image_width // 100,
                                                     h_abs * self.image_height // 100))
            elif self.image_mode == 'px':
                return pygame.transform.scale(self._image[self.image_index], (self.image_width, self.image_height))
            elif self.image_mode == '%img':
                w, h = self._image[self.image_index].get_width(), self._image[self.image_index].get_height()
                return pygame.transform.scale(self._image[self.image_index],
                                                    (w * self.image_width // 100,
                                                     h * self.image_height // 100))
        return self._image[self.image_index]

    def image_ready(self):
        """
        condition of image availability
        :return:
        """
        return bool(self._image)


class Object(Sizible, Image):

    def __init__(self,
                 resolution,
                 x_rel=0,
                 y_rel=0,
                 w_rel=0,
                 h_rel=0,
                 adopt_size=True,
                 adopt_cords=True,
                 border=None,
                 border_color=(0, 0, 0)):
        Sizible.__init__(self, x_rel, y_rel, w_rel, h_rel, adopt_size, adopt_cords)
        Image.__init__(self, None)
        """
        :param resolution:
        :param x_rel: x % if adopt_cords == True else px
        :param y_rel: y % if adopt_cords == True else px
        :param w_rel: w % if adopt_size == True else px
        :param h_rel: h % if adopt_size == True else px
        :param adopt_size: adaptation object for new resolution(if enabled:
        uses w_rel and h_rel as % of new resolution)
        :param adopt_cords: adaptation object for new resolution(if enabled:
        uses x_rel and y_rel as % of new resolution)
        :param border: border width
        :param border_color:
        """
        self.x_rel, self.y_rel, self.w_rel, self.h_rel = x_rel, y_rel, w_rel, h_rel  # relative

        self.adopt_size = adopt_size
        self.adopt_cords = adopt_cords

        # self.color = pygame.color.Color('black')
        self.color = None

        self.border_color = border_color
        self.border = border

        self.font_size = 16
        self.font = pygame.font.SysFont(DEFAULTFONT, self.font_size)
        self.text = None
        self.text_shift_x = 0
        self.text_shift_y = 0
        self.text_color = (0, 0, 0)

        self.adopt(resolution)

    def adopt(self, resolution: Tuple[int, int]):
        """
        Adaptation for new resolution
        :param resolution: new resolution
        :return:
        """
        super().adopt(resolution)

    def set_pos(self, x_rel=None, y_rel=None, adopt_cords=None, resolution=None):
        """
        set new position or change settings of positing
        :param x_rel:
        :param y_rel:
        :param adopt_cords:
        :param resolution:
        :return:
        """
        if x_rel:
            self.x_rel = x_rel
        if y_rel:
            self.y_rel = y_rel
        if adopt_cords:
            self.adopt_cords = adopt_cords
        if resolution:
            self.adopt(resolution)

    def get_rect(self) -> pygame.rect.RectType:
        """
        getting sizes of object
        :return: sizes
        """
        return pygame.rect.Rect(self.x, self.y, self.w, self.h)

    def set_color(self, color: Union[rgba, hsva], fmt: str = 'rgb'):
        """
        setting color
        :param color: color rgb or hsv
        :param fmt: format of color
        :return:
        """
        if fmt == 'hsv':
            self.color.hsva = color
        elif fmt == 'rgb':
            self.color.r, self.color.g, self.color.b = color[:3]
            if len(color) > 3:
                self.color.a = color[3]

    def check(self, x, y):
        """
        checking position(hover or click)
        :param x:
        :param y:
        :return:
        """
        return self.x <= x <= self.x + self.w and \
            self.y <= y <= self.h + self.y

    def connect_hover(self, action: Callable, delay=0.1):
        self.on_hover = action

    def hover(self, x, y):
        """
        calls on mouse_move
        :param x: of mouse
        :param y: of mouse
        :return:
        """
        if self.check(x, y):
            self.on_hover()

    def on_hover(self):
        pass

    def font_set(self, *args, **kwargs):
        """
        setting font
        :param args:
        :param kwargs:
        :return:
        """
        self.font = args[0] if isinstance(args[0], pygame.font.FontType) else \
            pygame.font.SysFont(*args, **kwargs)

    def text_set(self, text: str, text_color: rgb = None, shift_x: int = None, shift_y: int = None):
        """
        setting text and shifts
        :param text:
        :param text_color:
        :param shift_x: shift x
        :param shift_y: shift y
        :return:
        """
        if shift_x:
            self.text_shift_x = shift_x
            if self.adopt_size:
                self.text_shift_x *= self.w / 100
        if shift_y:
            self.text_shift_y = shift_y
            if self.adopt_size:
                self.text_shift_y *= self.h / 100
        if text_color:
            self.text_color = text_color
        if text:
            self.text = self.font.render(text, False, self.text_color)

    def mouse_down(self, x, y):
        ...

    def mouse_up(self, x, y):
        ...

    def mouse_move(self, x, y):
        ...

    def draw(self, screen):
        """
        just draw
        :param screen:
        :return:
        """
        if self.text:
            screen.blit(self.text, (self.x + self.text_shift_x, self.y + self.text_shift_y - round(self.font_size * 1.3) / 2))
        if self.color:
            pygame.draw.rect(screen, self.color, self.get_rect())
        if self.border:
            pygame.draw.rect(screen, self.border_color, self.get_rect(), self.border)
        if self.image_ready():
            screen.blit(self.image_render(self.w, self.h), self.get_rect())


class RadialObject(Object):
    """
    object but radial
    """

    def __init__(self,
                 resolution,
                 x_rel=0,
                 y_rel=0,
                 r_rel=0,
                 adopt_size=True,
                 adopt_cords=True,
                 adopt_order=0,
                 border=None,
                 border_color=(0, 0, 0)):
        super().__init__(resolution,
                         x_rel,
                         y_rel,
                         r_rel * 2 if not adopt_order else r_rel * 2 * resolution[0] // resolution[1],
                         r_rel * 2 if adopt_order else r_rel * 2 * resolution[1] // resolution[0],
                         adopt_size,
                         adopt_cords,
                         border,
                         border_color)
        self.r_rel = r_rel
        self.r = r_rel * resolution[adopt_order]
        self.xc, self.yc = self.x + self.r, self.y + self.r

    def check(self, x, y):
        """
        # probably need to optimize
        checking radial object
        :param x:
        :param y:
        :return:
        """
        return (x - self.xc) ** 2 + (y - self.yc) ** 2 <= self.r ** 2

    def draw(self, screen):
        if self.text:
            screen.blit(self.text, (self.x + self.text_shift_x, self.y + self.text_shift_y - round(self.font_size * 1.3) / 2))
        if self.color:
            pygame.draw.ellipse(screen, self.color, self.get_rect())
        if self.border:
            pygame.draw.ellipse(screen, self.border_color, self.get_rect(), self.border)
        if self.image_ready():
            screen.blit(self.image_render(self.w, self.h), self.get_rect())


class Button(Object):
    """
    Just button
    """
    def __init__(self,
                 resolution,
                 x_rel=0,
                 y_rel=0,
                 w_rel=0,
                 h_rel=0,
                 adopt_size=True,
                 adopt_cords=True,
                 border=None,
                 border_color=(0, 0, 0)):
        super().__init__(resolution,
                         x_rel,
                         y_rel,
                         w_rel,
                         h_rel,
                         adopt_size,
                         adopt_cords,
                         border,
                         border_color)

        self.action_on_mouse_down = None
        self.action_on_mouse_up = None
        self.color_on_mouse_up = self.color
        self.color_on_mouse_down = pygame.color.Color('Gray')
        self.image_on_mouse_up = None
        self.image_on_mouse_down = None

    def connect_mouse_down(self, action):
        self.action_on_mouse_down = action

    def connect_mouse_up(self, action):
        self.action_on_mouse_up = action

    def mouse_down(self, x, y):
        """
        foo must invoke on click
        :param x:
        :param y:
        :return:
        """
        if self.check(x, y):
            self.action_on_mouse_down()

    def mouse_up(self, x, y):
        """
        foo must invoke on click
        :param x:
        :param y:
        :return:
        """
        if self.check(x, y):
            self.action_on_mouse_up()


class Background(Image):

    """
    background as class for some reason...
    """
    def __init__(self, resolution, _image: str, w=100, h=100, mode='%res', x=0, y=0, scale=False):
        self._image = pygame.image.load(_image)
        self.scale = scale
        self.x, self.y = x, y
        self.w_rel, self.h_rel = w, h
        self.image = self.image_render(self.w, self.h)
        self.mode = mode
        self.adopt(resolution)

    def adopt(self, resolution):
        if self.scale:
            if self.mode == '%res':
                self.w, self.h = self.w_rel * resolution[0], self.h_rel * resolution[1]
            elif self.mode == 'px':
                self.w, self.h = resolution[0], resolution[1]
            elif self.mode == '%img' and self._image:
                self.w, self.h = self._image.get_width(), self._image.get_height()
            self.image = pygame.transform.scale(self.w, self.h)

    def get_rect(self):
        return self.x, self.y, self.w, self.h

    def draw(self, screen):
        screen.blit(self.image, self.get_rect())


class Sprite(pygame.sprite.Sprite, Sizible, Image):
    """
    Sprite or animated sprite
    """

    def __init__(self, x_rel, y_rel, w_rel, h_rel, adopt_size=True, adopt_cords=True, resolution=None, animated=False):
        self.animated = animated
        pygame.sprite.Sprite.__init__(self)
        Sizible.__init__(self, x_rel, y_rel, w_rel, h_rel, adopt_size, adopt_cords)
        Image.__init__(self, animated=animated)
        if resolution:
            self.adopt(resolution)
        self.image = self.image_render(self.w, self.h)  # None
        self.rect = self.get_rect()

    def set_image(self,
                  image_name: str = None,
                  width: int = 100,
                  height: int = 100,
                  size_mode: Union[percent_obj, percent_img, 'pixels'] = '%img',
                  index=0):
        super().set_image(image_name, width, height, size_mode, index)
        self.image = self.image_render(self.w, self.h)
        self.rect = self.get_rect()

    def resize(self, w_rel=None, h_rel=None, adopt_size=None, resolution=None):
        super().resize(w_rel, h_rel, adopt_size, resolution)
        self.image = self.image_render(self.w, self.h)
        self.rect = self.get_rect()

    def adopt(self, resolution):
        super().adopt(resolution)
        self.image = self.image_render(self.w, self.h)
        self.rect = self.get_rect()

    def get_rect(self) -> Tuple[int, int, int, int]:
        return self.x, self.y, self.w, self.h


class GameArea:
    """
    Class to control all objects
    """

    def __init__(self):
        self.objects = []
        self.sprites = pygame.sprite.Group()
        self.buttons = []
        self.mouse_click = None
        self.key_board_click = None
        self.background: Background = None
        self.background_music = []
        self.sounds: Dict[str, pygame.mixer.SoundType] = {}

    def set_background_music(self, *file_names):
        self.background_music = file_names

    def set_sounds(self, *file_names: str):
        """
        Compile sounds to play
        :param file_names: names of files
        :return:
        """
        for name in file_names:
            self.sounds[name[:name.rfind('.')]] = pygame.mixer.Sound(name)

    def add_objects(self, *objects):
        """
        adding object
        :param objects:
        :return:
        """
        for obj in objects:
            if isinstance(obj, pygame.sprite.Sprite):
                self.sprites.add(obj)
            elif isinstance(obj, Button):
                self.buttons.append(obj)
            elif isinstance(obj, Object):
                self.objects.append(obj)

    def render(self, screen):
        """
        drawing all objects
        :param screen:
        :return:
        """
        if self.background:
            self.background.draw(screen)
        for obj in self.objects:
            obj.draw(screen)
        for bt in self.buttons:
            bt.draw(screen)
        self.sprites.draw(screen)

    def change_resolution(self, resolution: Tuple[int, int]):
        """
        changing resolution for all objects
        :param resolution:
        :return:
        """
        for obj in self.objects:
            obj.adopt(resolution)
        for bt in self.buttons:
            bt.adopt(resolution)
        for sprite in self.sprites:
            sprite.adopt(resolution)

    def play_sound(self, sound: str, loops: int=0, maxtime: int=0, fade_ms: int=0):
        """
        Don't care how to invoke it from Object
        :param sound:
        :param loops:
        :param maxtime:
        :param fade_ms:
        :return:
        """
        self.sounds[sound].play(loops, maxtime, fade_ms)

    def on_mouse_click(self):
        pass

    def load(self):
        pass

    def connect_mouse_click(self, foo: Callable):
        """
        :param foo:
        :return:
        """
        self.mouse_click = foo

    def connect_keyboard_click(self, foo: Callable):
        self.key_board_click = foo