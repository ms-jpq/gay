#!/usr/bin/env python3


from argparse import ArgumentParser, Namespace
from atexit import register
from dataclasses import dataclass
from enum import Enum
from itertools import cycle, islice
from math import pi, sin
from os import environ
from random import choice, randint
from shutil import get_terminal_size
from sys import stdin, platform
from typing import Callable, Dict, Iterator, List, Tuple, cast
from unicodedata import east_asian_width
if platform == 'win32':
    from signal import signal, SIG_DFL
    from ctypes import windll
    WindowsColorTerm = True
    k=windll.kernel32
    k.SetConsoleMode(k.GetStdHandle(-11),7)
else:
    from signal import signal, SIGPIPE, SIG_DFL

class ColourSpace(Enum):
    EIGHT = "8"
    TRUE = "24"


class InterpolationMode(Enum):
    SHORT = "short"
    FULL = "full"


class Flags(Enum):
    LES = 1
    GAY = 2
    BI = 3
    TRANS = 4
    ACE = 5
    PAN = 6
    NB = 7
    GQ = 8


HexColour = str
RGB = Tuple[int, int, int]
RawPalette = List[Tuple[HexColour, int]]
Palette = List[RGB]
AspectRatio = Tuple[int, int]
Position = Tuple[int, int]
WindowsColorTerm = False


@dataclass
class FlagSpec:
    aspect_ratio: AspectRatio
    palette: RawPalette

DEFAULT_TERM_SIZE = (80, 80)

UNICODE_WIDTH_LOOKUP = {
    "W": 2,  # CJK
    "N": 0,  # Non printable
}

FLAG_SPECS: Dict[Flags, FlagSpec] = {
    Flags.LES: FlagSpec(
        aspect_ratio=(3, 5),
        palette=[
            ("#D62E02", 1),
            ("#FD9855", 1),
            ("#FFFFFF", 1),
            ("#D161A2", 1),
            ("#A20160", 1),
        ],
    ),
    Flags.GAY: FlagSpec(
        aspect_ratio=(3, 5),
        palette=[
            ("#FF0018", 1),
            ("#FFA52C", 1),
            ("#FFFF41", 1),
            ("#008018", 1),
            ("#0000F9", 1),
            ("#86007D", 1),
        ],
    ),
    Flags.BI: FlagSpec(
        aspect_ratio=(3, 5), palette=[
            ("#D60270", 2),
            ("#9B4F96", 1),
            ("#0038A8", 2)
        ],
    ),
    Flags.TRANS: FlagSpec(
        aspect_ratio=(3, 5),
        palette=[
            ("#55CDFC", 1),
            ("#F7A8B8", 1),
            ("#FFFFFF", 1),
            ("#F7A8B8", 1),
            ("#55CDFC", 1),
        ],
    ),
    Flags.ACE: FlagSpec(
        aspect_ratio=(3, 5),
        palette=[
            ("#000000", 1),
            ("#A4A4A4", 1),
            ("#FFFFFF", 1),
            ("#810081", 1)
        ],
    ),
    Flags.PAN: FlagSpec(
        aspect_ratio=(3, 5), palette=
        [
            ("#FF1B8D", 1),
            ("#FFDA00", 1),
            ("#1BB3FF", 1)
        ],
    ),
    Flags.NB: FlagSpec(
        aspect_ratio=(3, 5),
        palette=[
            ("#FFF430", 1),
            ("#FFFFFF", 1),
            ("#9C59D1", 1),
            ("#000000", 1)
        ],
    ),
    Flags.GQ: FlagSpec(
        aspect_ratio=(3, 5), palette=[
        ("#B77FDD", 1),
        ("#FFFFFF", 1),
        ("#48821E", 1)
        ]
    ),
}


def parse_args() -> Namespace:
    rand_flag = choice([f for f in Flags])
    colour_space = (
        ColourSpace.TRUE
        if environ.get("COLORTERM") in {"truecolor", "24bit"}
        else ColourSpace.EIGHT
    )
    namespace = Namespace(flag=rand_flag)
    parser = ArgumentParser()

    mode_group = parser.add_argument_group()
    mode_group.add_argument("-f", "--flag", dest="flag_only", action="store_true")

    flag_group = parser.add_argument_group()
    flag_group.add_argument(
        "-l", "--les", "--lesbian", action="store_const", dest="flag", const=Flags.LES,
    )
    flag_group.add_argument(
        "-g", "--gay", action="store_const", dest="flag", const=Flags.GAY,
    )
    flag_group.add_argument(
        "-b", "--bi", "--bisexual", action="store_const", dest="flag", const=Flags.BI,
    )
    flag_group.add_argument(
        "-t",
        "--trans",
        "--transgender",
        action="store_const",
        dest="flag",
        const=Flags.TRANS,
    )
    flag_group.add_argument(
        "-a", "--ace", "--asexual", action="store_const", dest="flag", const=Flags.ACE,
    )
    flag_group.add_argument(
        "-p",
        "--pan",
        "--pansexual",
        action="store_const",
        dest="flag",
        const=Flags.PAN,
    )
    flag_group.add_argument(
        "-n", "--nb", "--non-binary", action="store_const", dest="flag", const=Flags.NB,
    )
    flag_group.add_argument(
        "--gq", "--gender-queer", action="store_const", dest="flag", const=Flags.GQ,
    )

    opt_group = parser.add_argument_group()
    opt_group.add_argument(
        "-c",
        "--colour",
        choices=tuple(c.value for c in ColourSpace),
        default=colour_space.value,
    )
    opt_group.add_argument(
        "-i",
        "--interpolation",
        choices=tuple(i.value for i in InterpolationMode),
        default=InterpolationMode.FULL,
    )
    opt_group.add_argument(
        "--period", type=lambda i: abs(int(i)), default=randint(5, 10)
    )
    opt_group.add_argument("--tab-width", type=int, default=4)

    return parser.parse_args(namespace=namespace)


def on_exit() -> None:
    print("\x1b[0m", end="", flush=True)


def readlines() -> Iterator[str]:
    while True:
        line = stdin.readline()
        if line:
            yield line.rstrip()
        else:
            break


def flag_colours(flag: FlagSpec) -> Palette:
    return [parse_colour(p) for p, _ in flag.palette]


def parse_colour(colour: HexColour) -> RGB:
    hexc = colour[1:]
    it = iter(hexc)
    parsed = tuple(
        int(f"{h1}{h2}", 16) for h1, h2 in iter(lambda: tuple(islice(it, 2)), ())
    )
    return cast(RGB, parsed)


def decor_8(rgb: RGB) -> Iterator[str]:
    r, g, b = map(lambda c: int(round(c / 255 * 5)), rgb)
    yield str(16 + 36 * r + 6 * g + b)


def decor_24(rgb: RGB) -> Iterator[str]:
    r, g, b = map(str, rgb)
    yield r
    yield ";"
    yield g
    yield ";"
    yield b
    
    
def decor_for(space: ColourSpace) -> Tuple[str, str, Callable[[RGB], Iterator[str]]]:
    if space == ColourSpace.EIGHT and WindowsColorTerm == True:
        return "\x1b[38;5;", "\x1b[48;5;", decor_8
    elif space == ColourSpace.TRUE:
        return "\x1b[38;2;", "\x1b[48;2;", decor_24
    else:
        raise ValueError()


def paint_flag(colour_space: ColourSpace, spec: FlagSpec) -> Iterator[str]:
    cols, rows = get_terminal_size(DEFAULT_TERM_SIZE)
    _, bg_esc, decor = decor_for(colour_space)
    r, c = spec.aspect_ratio
    height = sum(h for _, h in spec.palette)
    ratio = r / c * 0.5
    multiplier = int(min((rows - 4) / height, cols / height * ratio))
    m = max(multiplier, 1)
    line = " " * cols
    for hexc, l in spec.palette:
        colour = parse_colour(hexc)
        for _ in range(0, l * m):
            yield bg_esc
            yield from decor(colour)
            yield "m"
            yield line
            yield "\x1b[0m"
            yield "\n"


def lerp(c1: RGB, c2: RGB, mix: float) -> RGB:
    lhs = map(lambda c: c * mix, c1)
    rhs = map(lambda c: c * (1 - mix), c2)
    new = map(lambda c: int(round(sum(c))), zip(lhs, rhs))
    return cast(RGB, tuple(new))


def unicode_width(char: str) -> int:
    try:
        code = east_asian_width(char)
        return UNICODE_WIDTH_LOOKUP.get(code, 1)
    except Exception:
        return 1


def enumerate_pos(
    tab_width: int, lines: Iterator[str],
) -> Iterator[Iterator[Tuple[Position, str]]]:
    cols, _ = get_terminal_size(DEFAULT_TERM_SIZE)
    x, y = 0, 0
    for line in lines:
        x, y = 0, y + 1

        def gen() -> Iterator[Tuple[Position, str]]:
            nonlocal x, y
            for char in line:
                if char == "\t":
                    char = " " * tab_width
                    x += tab_width
                else:
                    x += unicode_width(char)
                if x >= cols:
                    x, y = x - cols, y + 1
                yield (x, y), char

        yield gen()


def rgb_gen(palette: Palette, rep: int) -> Iterator[RGB]:
    gen = cycle(palette)

    period = pi * pi / 2

    def wave(t: float) -> float:
        x = t / rep * period
        return sin(x / pi + pi / 2)

    prev = next(gen)
    while True:
        curr = next(gen)
        for t in range(0, rep + 1):
            mix = wave(t)
            yield lerp(prev, curr, mix)
        prev = curr


def colourize(
    colour_space: ColourSpace,
    spec: FlagSpec,
    tab_width: int,
    period: int,
    lines: Iterator[str],
) -> Iterator[Iterator[str]]:
    palette = flag_colours(spec)
    colour_gen = rgb_gen(palette, period)
    fg_esc, _, decor = decor_for(colour_space)
    for line in enumerate_pos(tab_width, lines):

        def gen() -> Iterator[str]:
            for _, char in line:
                colour = next(colour_gen)
                yield fg_esc
                yield from decor(colour)
                yield "m"
                yield char
            yield "\x1b[0m"
            yield "\n"

        yield gen()


def main() -> None:
    if platform != 'win32':
      signal(SIGPIPE, SIG_DFL)
    args = parse_args()
    register(on_exit)
    colour_space = ColourSpace(args.colour)
    spec = FLAG_SPECS[args.flag]

    if args.flag_only:
        flag_stripes = paint_flag(colour_space=colour_space, spec=spec)
        print(*flag_stripes, sep="", end="")
    else:
        lines = readlines()
        # interpolation = InterpolationMode(args.interpolation)
        period = max(5, args.period) if args.period else 5

        gen = colourize(
            colour_space=colour_space,
            spec=spec,
            tab_width=args.tab_width,
            period=period,
            lines=lines,
        )
        for new_line in gen:
            print(*new_line, sep="", end="")


try:
    main()
except KeyboardInterrupt:
    exit(130)
