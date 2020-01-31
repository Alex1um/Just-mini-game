from typing import *
import pygame

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

    def render(self):
        pass


class Sizible:
    """
    Object with sizes and cords
    """
    def __init__(self,
                 x_rel=0,
                 y_rel=0,
                 w_rel=1,
                 h_rel=1,
                 adopt_size=True,
                 adopt_cords=True,
                 adopt_order=None):
        self.x, self.y = None, None
        self.w, self.h = None, None
        self.x_rel = x_rel
        self.y_rel = y_rel
        self.w_rel = w_rel
        self.h_rel = h_rel
        self.adopt_size = adopt_size
        self.adopt_cords = adopt_cords
        self.adopt_order = adopt_order

    def adopt(self, resolution):
        if self.adopt_cords:
            self.x = round(self.x_rel * resolution[0] / 100)
            self.y = round(self.y_rel * resolution[1] / 100)
        if self.adopt_size:
            if self.adopt_order is not None:
                resolution = (
                    resolution[self.adopt_order],
                    resolution[self.adopt_order])
            self.w = round(self.w_rel * resolution[0] / 100)
            self.h = round(self.h_rel * resolution[1] / 100)

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
                 file_name: Union[str, Iterable] = None,
                 width=100,
                 height=100,
                 mode: Union[percent_img, percent_obj, pixels] = '%img',
                 animated: bool = False,
                 animation_delay_frames: int = 0):
        """
        init image
        :param file_name: name of file
        :param width: width % or px
        :param height: height % or px
        :param mode: mode to scale image
        :param animated: is it animation
        :param animation_delay_frames: delay for switching frames if animated
        """
        self._image = []
        if file_name:
            # self._image = [pygame.image.load(file_name)]
            self.add_images(file_name)
        self.animation_delay_frames = animation_delay_frames
        self._frame = 0
        self.image_animated = animated
        self.image_index = 0
        self.image_width = width
        self.image_height = height
        self.image_mode = mode
        self.image_enabled = True
        self.image_rotation = None

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
                  index=0,
                  rotation=None):
        """
        setting image or image params
        :param image_name: name of new image
        :param width:
        :param height:
        :param size_mode: mode for rescale
        :param index: index of image
        :param rotation: angle for rotate image(s)
        :return:
        """
        if rotation:
            self.image_rotation = rotation
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

    def image_render(self,
                     w_abs: int = None,
                     h_abs: int = None) -> pygame.SurfaceType:
        """
        render image with current mode
        :param w_abs: width of object to scale image
        :param h_abs: height of object to scale image
        :return: image
        """
        if self.image_animated:
            if self._frame == self.animation_delay_frames:
                self.image_index = (self.image_index + 1) % len(self._image)
                self._frame = 0
            else:
                self._frame += 1
        if self._image:
            img = self._image[self.image_index]
            if self.image_rotation:
                img = pygame.transform.rotate(img, self.image_rotation)
            if self.image_mode == '%obj':
                return pygame.transform.scale(img,
                                              (
                                                  round(
                                                      w_abs * self.image_width
                                                      / 100),
                                                  round(
                                                   h_abs * self.image_height
                                                   / 100)
                                               ))
            elif self.image_mode == 'px':
                return pygame.transform.scale(img,
                                              (self.image_width,
                                               self.image_height
                                               ))
            elif self.image_mode == '%img':
                w, h = img.get_width(), img.get_height()
                return pygame.transform.scale(img,
                                              (round(w * self.image_width
                                                     / 100),
                                               round(h * self.image_height
                                                     / 100)
                                               ))
        return self._image[self.image_index]

    def image_ready(self):
        """
        condition of image availability
        :return:
        """
        return bool(self._image) and self.image_enabled

    def get_image_rect(self, image=None) -> Tuple[int, int]:
        return image.get_rect() if image else self._image[0].get_rect()


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
                 border_color=(0, 0, 0),
                 adopt_order=None,
                 font_scale=100):
        Sizible.__init__(self,
                         x_rel,
                         y_rel,
                         w_rel,
                         h_rel,
                         adopt_size,
                         adopt_cords,
                         adopt_order)
        Image.__init__(self, None)
        self.enable = True
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
        self.x_rel, self.y_rel = x_rel, y_rel
        self.w_rel, self.h_rel = w_rel, h_rel  # relative

        self.font = None
        self.text = None
        self.font_scale = font_scale
        self.adopt_size = adopt_size
        self.adopt_cords = adopt_cords

        self.color = None
        # self.color = None

        self.border_color = border_color
        self.border = border

        self.adopt(resolution)
        self._text = None
        self.text_align = 'center'
        self.text_valign = 'center'
        self.text_pos = None
        self.text_color = (0, 0, 0)

        self._hovered = False

    def not_hover(self, e, x, y):
        pass

    def on_hover(self, e, x, y):
        pass

    def on_key_down(self, key):
        pass

    def on_key_up(self, key):
        pass

    def on_mouse_up(self, x, y, key):
        pass

    def on_mouse_down(self, x, y, key):
        pass

    def adopt(self, resolution: Tuple[int, int]):
        """
        Adaptation for new resolution
        :param resolution: new resolution
        :return:
        """
        super().adopt(resolution)
        if self.adopt_size:
            self.font = pygame.font.SysFont(
                DEFAULTFONT,
                round(min(self.w, self.h) * 0.75) * self.font_scale // 100)
            if self.text is not None:
                self._text = self.text_render()

    def text_render(self, aa=False):
        return self.font.render(self.text, aa, self.text_color)

    def set_pos(self,
                x_rel=None,
                y_rel=None,
                adopt_cords=None,
                resolution=None):
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

    def set_color(self,
                  color: Union[rgba, hsva, pygame.color.Color],
                  fmt: str = 'rgb'):
        """
        setting color
        :param color: color rgb or hsv
        :param fmt: format of color
        :return:
        """
        if color and self.color is None:
            self.color = pygame.Color('black')
        if isinstance(color, pygame.color.Color):
            self.color = color
        elif fmt == 'hsv' and color:
            self.color.hsva = color
        elif fmt == 'rgb' and color:
            self.color.r, self.color.g, self.color.b = color[:3]
            if len(color) > 3:
                self.color.a = color[3]

    def check(self, x, y, *cords):
        """
        checking position(hover or click)
        :param x:
        :param y:
        :return:
        """
        if cords:
            for i in range(0, len(cords), 2):
                other = self.x <= cords[i] <= self.x + self.w and\
                        self.y <= cords[i + 1] <= self.h + self.y
                if other:
                    return other
        return self.x <= x <= self.x + self.w and self.y <= y <= self.h + self.y

    def hover(self, x, y):
        """
        calls on mouse_move
        :param x: of mouse
        :param y: of mouse
        :return:
        """
        if self.enable:
            if self.check(x, y):
                self.on_hover(self, x, y)
                self._hovered = True
            elif self._hovered:
                self.not_hover(self, x, y)
                self._hovered = False

    def set_font(self, *args, font_scale=None, **kwargs):
        """
        Setting font
        :param args:
        :param font_scale:
        :param kwargs:
        :return:
        """
        if self.font_scale:
            self.font_scale = font_scale
        if args:
            self.font = args[0] if isinstance(args[0],
                                              pygame.font.FontType) else \
                pygame.font.SysFont(*args, **kwargs)

    def set_text(self,
                 text: str = None,
                 text_color: rgb = None,
                 align: str = None,
                 valign: str = None,
                 text_pos: str = None):
        """
        setting text and rendering
        :param text:
        :param text_color:
        :param align:
        :param valign:
        :param text_pos:
        :return:
        """
        if align:
            self.text_align = align
        if valign:
            self.text_valign = valign
        if text_color:
            self.text_color = text_color
        if text is not None:
            self.text = text
            self._text = self.text_render()
        if text_pos:
            self.text_pos = text_pos

    def draw(self, screen):
        """
        just draw
        :param screen:
        :return:
        """
        if self.enable:
            if self.color:
                pygame.draw.rect(screen, self.color, self.get_rect())
            if self.border:
                pygame.draw.rect(
                    screen,
                    self.border_color,
                    self.get_rect(),
                    self.border
                )
            if self.image_ready():
                screen.blit(self.image_render(self.w, self.h), self.get_rect())
            if self.text is not None:
                x, y, w, h = self._text.get_rect(
                    center=(self.w // 2 + self.x, self.h // 2 + self.y))
                if self.text_align == 'left':
                    x = self.x + 5
                elif self.text_align == 'right':
                    x = self.x + self.w - 5 - w
                if self.text_valign == 'top':
                    y = self.y + 5
                elif self.text_valign == 'bottom':
                    y = self.y + self.h - 5 - h
                if self.text_pos == 'right':
                    x += self.w
                screen.blit(self._text, (x, y, w, h))


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
                 border_color=(0, 0, 0),
                 font_scale=100):
        self.r_rel = r_rel // 2 + 0.5
        self.r = round(r_rel * resolution[adopt_order] / 100)
        super().__init__(resolution,
                         x_rel,
                         y_rel,
                         r_rel,
                         r_rel,
                         adopt_size,
                         adopt_cords,
                         border,
                         border_color,
                         adopt_order,
                         font_scale)
        self.xc, self.yc = self.x + self.r, self.y + self.r

    def adopt(self, resolution: Tuple[int, int]):
        super().adopt(resolution)
        self.xc, self.yc = self.x + self.r, self.y + self.r
        self.r = round(self.r_rel * resolution[self.adopt_order] / 100)

    def check(self, x, y, *cords):
        """
        # probably need to optimize
        checking radial object
        :param x:
        :param y:
        :return:
        """
        if cords:
            for i in range(0, len(cords), 2):
                other = self.x <= cords[i] <= self.x + self.w and\
                        self.y <= cords[i + 1] <= self.h + self.y
                if other:
                    return other
        return (x - self.xc) ** 2 + (y - self.yc) ** 2 <= self.r ** 2

    def draw(self, screen):
        if self.color:
            pygame.draw.ellipse(screen, self.color, self.get_rect())
        if self.border:
            pygame.draw.ellipse(
                screen,
                self.border_color,
                self.get_rect(),
                self.border
            )
        if self.image_ready():
            screen.blit(self.image_render(self.w, self.h), self.get_rect())
        if self.text:
            x, y, w, h = self._text.get_rect(
                center=(self.w // 2 + self.x, self.h // 2 + self.y))
            if self.text_align == 'left':
                x = self.x + 5
            elif self.text_align == 'right':
                x = self.x + self.w - 5
            if self.text_valign == 'top':
                y = self.y + 5
            elif self.text_valign == 'bottom':
                y = self.y + self.h - 5
            if self.text_pos == 'right':
                x += self.w
            elif self.text_pos == 'left':
                x -= w + 5
            screen.blit(self._text, (x, y, w, h))


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
                 border_color=(0, 0, 0),
                 adopt_order=None,
                 font_scale=100):
        super().__init__(resolution,
                         x_rel,
                         y_rel,
                         w_rel,
                         h_rel,
                         adopt_size,
                         adopt_cords,
                         border,
                         border_color,
                         adopt_order,
                         font_scale)

        self.action_on_mouse_down = nothing
        self.action_on_mouse_up = nothing
        self.color_on_mouse_down = (220, 220, 220)
        self.color_on_mouse_up = self.color
        self._pressed = False

    def connect_mouse_down(self, action):
        self.action_on_mouse_down = action

    def connect_mouse_up(self, action):
        self.action_on_mouse_up = action

    def on_mouse_down(self, x, y, key):
        """
        checking mouse position and do binded action
        :param x:
        :param y:
        :param key: mouse button
        :return:
        """
        if self.check(x, y):
            self.set_color(self.color_on_mouse_down)
            self.action_on_mouse_down(self)
            self._pressed = True

    def hover(self, x, y):
        if self.check(x, y):
            if not self._pressed:
                self.on_hover(self, x, y)
            self._hovered = True
            return
        elif self._hovered:
            self.not_hover(self, x, y)
            self._pressed = False
            self.set_color(self.color_on_mouse_up)
            self._hovered = False

    def on_mouse_up(self, x, y, key):
        """
        checking mouse pos and do binded action
        :param x:
        :param y:
        :param key: mouse button
        :return:
        """
        if self.check(x, y):
            self.set_color(self.color_on_mouse_up)
            self.action_on_mouse_up(self)
            self._pressed = False


class Background(Image):

    """
    background as class for some reason...
    """
    def __init__(self,
                 resolution,
                 image_name: Union[str, Iterable],
                 animated=False,
                 frame_delay=0,
                 w=100,
                 h=100,
                 mode='%obj',
                 x=0,
                 y=0,
                 scale=False):
        Image.__init__(self,
                       image_name,
                       animated=animated,
                       animation_delay_frames=frame_delay)
        self.scale = scale
        self.x, self.y = x, y
        self.w, self.h = None, None
        self.w_rel, self.h_rel = w, h
        self.adopt(resolution)
        self.image_mode = mode

    def adopt(self, resolution):
        self.w = round(resolution[0] * self.w_rel / 100)
        self.h = round(resolution[1] * self.h_rel / 100)

    def get_rect(self):
        return self.x, self.y, self.w, self.h

    def draw(self, screen):
        if self.image_ready():
            screen.blit(self.image_render(self.w, self.h), self.get_rect())
        else:
            pygame.draw.rect(screen, (255, 255, 255), self.get_rect())


class Sprite(pygame.sprite.Sprite, Sizible, Image):
    """
    Sprite or animated sprite
    """

    def __init__(self,
                 resolution,
                 image,
                 x_rel,
                 y_rel,
                 w_rel,
                 h_rel,
                 adopt_size=True,
                 adopt_cords=True,
                 animated=False):
        self.animated = animated
        pygame.sprite.Sprite.__init__(self)
        Sizible.__init__(self,
                         x_rel,
                         y_rel,
                         w_rel,
                         h_rel,
                         adopt_size,
                         adopt_cords)
        Image.__init__(self, image, animated=animated)
        if resolution:
            self.adopt(resolution)
        self.image = self.image_render(self.w, self.h)  # None
        self.rect = self.get_rect()

    def set_image(self,
                  image_name: str = None,
                  width: int = 100,
                  height: int = 100,
                  size_mode: Union[percent_obj, percent_img, 'pixels'] = '%img',
                  index=0,
                  rotation=None):
        super().set_image(image_name, width, height, size_mode, index, rotation)
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


class TextEdit(Object):

    def __init__(self,
                 resolution,
                 x_rel=0,
                 y_rel=0,
                 w_rel=0,
                 h_rel=0,
                 adopt_size=True,
                 adopt_cords=True,
                 border=None,
                 border_color=(255, 255, 255),
                 adopt_order=None,
                 font_scale=100):
        super().__init__(resolution,
                         x_rel,
                         y_rel,
                         w_rel,
                         h_rel,
                         adopt_size,
                         adopt_cords,
                         border,
                         border_color,
                         adopt_order,
                         font_scale)
        self.high = False
        self.set_text('', text_color=(255, 255, 255), align='left')
        self.color_filling = (200, 200, 200)
        self.color_default = self.color
        self.delay = 1000
        self.text_condition: Callable = lambda *args: True

    def on_mouse_up(self, x, y, key):
        if self.check(x, y):
            self.high = True
            self.set_color(self.color_filling)
            self.set_text(self.text)
        elif self.high:
            self.high = False
            self.set_color(self.color_default)
            self.set_text(self.text)

    def on_key_down(self, key: str):
        if self.high:
            if self.text_condition(self, key):
                self.set_text(self.text + key)
            elif key == 'backspace':
                self.set_text(self.text[:-1])

    def draw(self, screen):
        super().draw(screen)

    def text_render(self, aa=False):
        return self.font.render(
            self.text + '|' if self.high else self.text,
            aa,
            self.text_color
        )


class MovableObject(Object):

    def __init__(self,
                 resolution,
                 x_rel=0,
                 y_rel=0,
                 w_rel=0,
                 h_rel=0,
                 adopt_size=True,
                 adopt_cords=True,
                 border=None,
                 border_color=(0, 0, 0),
                 adopt_order=None,
                 font_scale=100):
        super().__init__(resolution,
                         x_rel,
                         y_rel,
                         w_rel,
                         h_rel,
                         adopt_size,
                         adopt_cords,
                         border,
                         border_color,
                         adopt_order,
                         font_scale)
        self.grabbed = False
        self.sx, self.sy = self.x, self.y
        self.grabbed_x = None
        self.grabbed_y = None

    def on_mouse_down(self, x, y, key):
        if self.check(x, y):
            self.grabbed = True
            self.sx, self.sy = self.x, self.y
            self.grabbed_x = x
            self.grabbed_y = y

    def on_mouse_up(self, x, y, key):
        self.grabbed = False

    def hover(self, x, y):
        if self.grabbed:
            self.x = self.x + x - self.grabbed_x
            self.y = self.y + y - self.grabbed_y
            self.grabbed_x = x
            self.grabbed_y = y


class StatusBar(Object):

    def __init__(self,
                 resolution,
                 status=100,
                 x_rel=0,
                 y_rel=0,
                 w_rel=0,
                 h_rel=0,
                 adopt_size=True,
                 adopt_cords=True,
                 border=None,
                 border_color=(0, 0, 0),
                 adopt_order=None,
                 font_scale=100):
        super().__init__(resolution,
                         x_rel,
                         y_rel,
                         w_rel,
                         h_rel,
                         adopt_size,
                         adopt_cords,
                         border,
                         border_color,
                         adopt_order,
                         font_scale)
        if status < 0:
            status = 0
        status /= 100
        self.bar = Object(resolution,
                          x_rel,
                          y_rel,
                          w_rel * status,
                          h_rel,
                          adopt_size=adopt_size,
                          adopt_cords=adopt_cords,
                          adopt_order=adopt_order)
        self.bar.set_color((120 * status, 100, 100), 'hsv')

    def set_status(self, status):
        if status < 0:
            status = 0
        status /= 100
        self.bar.set_color((120 * status, 100, 100), 'hsv')
        self.bar.resize(self.w_rel * status, self.h_rel)

    def draw(self, screen):
        super().draw(screen)
        self.bar.draw(screen)


class GameArea:
    """
    Class to control all objects
    """

    def __init__(self):
        self.objects: List[Object] = []
        self.sprites = pygame.sprite.Group()
        self.background: Background = None
        self.background_music = []
        self.sounds: Dict[str, pygame.mixer.SoundType] = {}
        self.interface: Interface = None

    def update(self, main):
        pass

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
        self.sprites.draw(screen)
        if self.interface:
            self.interface.render()

    def change_resolution(self, resolution: Tuple[int, int]):
        """
        changing resolution for all objects
        :param resolution:
        :return:
        """
        if self.background:
            self.background.adopt(resolution)
        for obj in self.objects:
            obj.adopt(resolution)
        for sprite in self.sprites:
            sprite.adopt(resolution)

    def play_sound(self,
                   sound: str, 
                   loops: int = 0,
                   maxtime: int = 0, 
                   fade_ms: int = 0):
        """
        Don't care how to invoke it from Object
        :param sound:
        :param loops:
        :param maxtime:
        :param fade_ms:
        :return:
        """
        self.sounds[sound].play(loops, maxtime, fade_ms)

    def on_mouse_up(self, x, y, key):
        for obj in self.objects:
            obj.on_mouse_up(x, y, key)

    def on_mouse_down(self, x, y, key):
        for obj in self.objects:
            obj.on_mouse_down(x, y, key)

    def on_mouse_motion(self, x, y):
        for obj in self.objects:
            obj.hover(x, y)

    def on_key_up(self, key):
        for obj in self.objects:
            obj.on_key_up(key)

    def on_key_down(self, key):
        for obj in self.objects:
            obj.on_key_down(key)

    def load(self, resolution):
        self.change_resolution(resolution)
