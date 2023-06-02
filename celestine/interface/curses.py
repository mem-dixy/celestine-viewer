""""""

import PIL.Image
from PIL import Image
from typing import Tuple, Type, List

import io
import math
import random

from celestine import load
from celestine.package import pillow
from celestine.package.curses import package as curses
from celestine.unicode import LINE_FEED
from celestine.unicode.notational_systems import BRAILLE_PATTERNS
from celestine.window.element import Abstract as abstract
from celestine.window.element import Button as button
from celestine.window.element import Image as image
from celestine.window.element import Label as label
from celestine.window.window import Window as window

color_table = {}
TEST = 0


def test_pillow(
    img_input: Image.Image, method: int
) -> Tuple[Type[Image.Image], List[List[int]]]:

    img = img_input

    threshold_pixel_percentage: float = 0.05
    nb_colours: int = 20
    nb_colours_under_threshold: int
    nb_pixels: int = img.width * img.height
    quantized_img: Image.Image

    while True:
        # method 0 = median cut 1 = maximum coverage 2 = fast octree
        quantized_img = img.quantize(colors=nb_colours, method=method, kmeans=0)
        nb_colours_under_threshold = 0
        colours_list: [Tuple[int, int]] = quantized_img.getcolors(nb_colours)
        for (count, pixel) in colours_list:
            if count / nb_pixels < threshold_pixel_percentage:
                nb_colours_under_threshold += 1
        if nb_colours_under_threshold == 0:
            break
        nb_colours -= -(-nb_colours_under_threshold // 2)  # ceil integer division
    palette: [int] = quantized_img.getpalette()
    colours_list: [[int]] = [palette[i : i + 3] for i in range(0, nb_colours * 3, 3)]
    return quantized_img, colours_list



def start_color():
    global color_table

    print(curses.COLORS)
    print(curses.COLOR_PAIRS)


    reserved = 8

    limit = min(curses.COLORS, curses.COLOR_PAIRS)
    # 8 reserved colors. Remaining split over 3 channels.
    split = (limit - reserved) ** (1/3)
    base = math.floor(split)

    power_zero = base ** 0
    power_one = base ** 1
    power_two = base ** 2
    power_three = base ** 3

    scale = 1000 // (base - 1)

    for index in range(reserved, reserved + power_three):
        color = index - reserved

        red = ((color // power_zero) % base) * scale
        green = ((color // power_one) % base) * scale
        blue = ((color // power_two) % base) * scale

        red1 = color // power_zero
        green1 = color // power_one
        blue1 = color // power_two


        red2 = red1 % base
        green2 = green1 % base
        blue2 = blue1 % base


        red3 = red2 * scale
        green3 = green2 * scale
        blue3 = blue2 * scale


        curses.init_color(index, red, green, blue)
        curses.init_pair(index, index, 0)

        color_table[(red2, green2, blue2)] = index



def round_a_color(color):

    reserved = 8
    limit = min(curses.COLORS, curses.COLOR_PAIRS)
    # 8 reserved colors. Remaining split over 3 channels.
    split = (limit - reserved) ** (1/3)
    base = math.floor(split)


    color /= 255
    color *= (base -1)
    color = round(color)
    color = int(color)

    return color


def round_colors(color):
    global color_table

    red, green, blue = color

    red = round_a_color(red)
    green = round_a_color(green)
    blue = round_a_color(blue)



    index = color_table[(red, green, blue)]

    return index



class Abstract(abstract):
    """"""

    def add_string(self, frame, x_dot, y_dot, text, *extra):
        """Curses swaps x and y."""
        frame.addstr(y_dot, x_dot, text, *extra)

    def origin(self):
        """"""
        x_dot = int(self.x_min)
        y_dot = int(self.y_min)
        return (x_dot, y_dot)

    def render(self, collection, item, **star):
        """"""
        text = item
        (x_dot, y_dot) = self.origin()
        self.add_string(collection, x_dot, y_dot, text)


class Button(Abstract, button):
    """"""

    def draw(self, collection, **star):
        """"""
        item = f"button:{self.data}"
        self.render(collection, item, **star)


class Image(Abstract, image):
    """"""

    def output(self):



        pixels = list(self.cache.getdata())
        string = io.StringIO()

        def shift(offset_x, offset_y):
            nonlocal braille
            nonlocal range_x
            nonlocal range_y

            index_x = range_x + offset_x
            index_y = range_y + offset_y

            index = index_y * self.width + index_x
            pixel = pixels[index] // 255

            braille <<= 1
            braille |= pixel

        for range_y in range(0, self.height, 4):
            for range_x in range(0, self.width, 2):
                braille = 0

                shift(0, 0)
                shift(1, 0)
                shift(0, 1)
                shift(1, 1)
                shift(0, 2)
                shift(1, 2)
                shift(0, 3)
                shift(1, 3)

                text = BRAILLE_PATTERNS[braille]
                string.write(text)

            string.write(LINE_FEED)

        value = string.getvalue()
        value = value[0:-1]
        return value.split(LINE_FEED)

    def render(self, collection, item, **star):
        """"""
        (x_dot, y_dot) = self.origin()

        color = list(self.color.getdata())

        index_y = 0
        for row_text in item:
            #print(f"({row_text})")

            index_x = 0
            for col_text in row_text:
                #print(f"<{col_text}>")


                width, height = self.color.size
                index = index_y * width + index_x
                pretty = color[index]

                ugly = round_colors(pretty)



                index = random.randrange(8,72)
                extra = curses.color_pair(index)

                extra = curses.color_pair(ugly)

                self.add_string(
                    collection,
                    x_dot +index_x,
                    y_dot + index_y,
                    col_text,
                    extra,
                )

                index_x += 1

            index_y += 1


    def draw(self, collection, **star):
        """"""
        global TEST
        path = self.image or load.asset("null.png")

        self.cache = pillow.Image.load(path)
        self.color = pillow.Image.clone(self.cache)


        width, height = self.resize(self.cache.image.width, self.cache.image.height)



        source_length_x = self.cache.image.width
        source_length_y = self.cache.image.height

        length_x = self.x_max - self.x_min
        length_y = self.y_max - self.y_min

        target_length_x = length_x * 2
        target_length_y = length_y * 4


        source_length = (source_length_x, source_length_y)
        target_length = (target_length_x, target_length_y)

        box = self.crop(source_length, target_length)

        if TEST == 11 * 10:

            #self.cache.image.show()
            self.cache.image.save("cat.png")


            dog, cow = test_pillow( self.cache.image, 0)
            dog.save("dog.png")
            print(dog, cow)


            colors = 15 # 17 - 256
            method = PIL.Image.Quantize.MEDIANCUT
            kmeans = 0
            palette = None
            dither = PIL.Image.Dither.FLOYDSTEINBERG

            self.cache.image = self.cache.image.quantize(
                colors, method, kmeans, palette, dither
            )
            self.cache.image.save("pig.png")
            self.cache.convert_to_color()
            self.cache.image.show()

            #self.cache.image.show()




        self.cache.resize(target_length_x, target_length_y, box)
        self.color.resize(length_x, length_y, box)



        colors = 15 # 17 - 256
        method = PIL.Image.Quantize.MEDIANCUT
        kmeans = 0
        palette = None
        dither = PIL.Image.Dither.FLOYDSTEINBERG

        #self.color.image = self.color.image.quantize(
        self_color_image = self.color.image.quantize(
            colors, method, kmeans, palette, dither
        )


        self.cache.convert_to_mono()
        self.color.convert_to_color()

        self.width, self.height = self.cache.size


        item = self.output()
        self.render(collection, item, **star)

        TEST += 1



class Label(Abstract, label):
    """"""

    def draw(self, collection, **star):
        """"""
        item = f"label:{self.data}"
        self.render(collection, item, **star)


class Window(window):
    """"""

    def data(self, container):
        """"""
        container.data = curses.window(
            1,
            1,
            self.width - 1,
            self.height - 2,
        )

    def draw(self, **star):
        """"""
        self.data(self.page)

        super().draw(**star)

        self.stdscr.noutrefresh()
        self.background.noutrefresh()
        self.page.data.noutrefresh()
        curses.doupdate()

    def __enter__(self):
        super().__enter__()

        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(1)
        curses.start_color()
        start_color()

        self.background = curses.window(0, 0, self.width, self.height)
        self.background.box()

        header = curses.subwindow(
            self.background, 1, 0, self.width - 2, 1
        )
        header.addstr(self.session.language.APPLICATION_TITLE)

        footer = curses.subwindow(
            self.background, 1, self.height - 1, self.width - 2, 1
        )
        footer.addstr(self.session.language.CURSES_EXIT)

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback)
        while True:
            event = self.stdscr.getch()
            match event:
                case 258 | 259 | 260 | 261 as key:
                    match key:
                        case curses.KEY_UP:
                            self.cord_y -= 1
                        case curses.KEY_DOWN:
                            self.cord_y += 1
                        case curses.KEY_LEFT:
                            self.cord_x -= 1
                        case curses.KEY_RIGHT:
                            self.cord_x += 1

                    self.cord_x %= self.width
                    self.cord_y %= self.height
                    self.stdscr.move(self.cord_y, self.cord_x)
                case curses.KEY_EXIT:
                    break
                case curses.KEY_CLICK:
                    (x_dot, y_dot) = (
                        self.cord_x - 1,
                        self.cord_y - 1,
                    )
                    self.page.poke(x_dot, y_dot)

        self.stdscr.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()
        return False




    def __init__(self, session, element, size, **star):
        super().__init__(session, element, size, **star)
        self.background = None
        self.cord_x = 0
        self.cord_y = 0
        self.frame = None
        self.stdscr = None


def image_format():
    """"""
    return [
        ".bmp",
        ".sgi",
        ".rgb",
        ".bw",
        ".png",
        ".jpg",
        ".jpeg",
        ".jp2",
        ".j2c",
        ".tga",
        ".cin",
        ".dpx",
        ".exr",
        ".hdr",
        ".tif",
        ".tiff",
        ".webp",
        ".pbm",
        ".pgm",
        ".ppm",
        ".pnm",
        ".gif",
        ".png",
    ]


def window(session, **star):
    """"""
    element = {
        "button": Button,
        "image": Image,
        "label": Label,
    }
    size = (80, 24)
    size = (122, 35)
    return Window(session, element, size, **star)
