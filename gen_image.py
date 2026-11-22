# makefun anchor 167b5782 round 3
"""Akun Utama — news-image-20261122, entry 3/3: "THE DAY IN NUMBERS".

One 1024x1024 front page summing up Sunday 22 November 2026: a dark
numbers box plus a UTC timeline strip, three illustrated hero stories
(COP31, Bahrain, tonight's 148-drone barrage over Ukraine), ten more
panels, a dotted world map with pins 1-13, 25 more stories, a region
bar totalling 38, and a date check. All figures follow the verified
story set in POLA-STRATEGI-3of3.md. Painted with Pillow only.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (247, 241, 222)
PAPER = (252, 248, 235)
INK = (26, 26, 26)
RED = (176, 30, 36)
DARKRED = (140, 22, 28)
NAVY = (22, 40, 62)
NAVY2 = (16, 30, 48)
GOLD = (214, 178, 94)
SEA = (207, 226, 236)
LAND = (138, 154, 123)
GREY = (90, 88, 80)
LIGHTGREY = (120, 118, 108)

F_SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
F_SERIF_R = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
F_SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
F_SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy wrap by measured width; returns list of lines."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def vgrad(draw, box, top, bottom):
    x0, y0, x1, y1 = box
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0)
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        draw.line([(x0, y), (x1, y)], fill=c)


def burst(draw, cx, cy, r, core=(255, 190, 60), mid=(240, 110, 30), outer=(200, 60, 20)):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=outer)
    draw.ellipse([cx - r * 0.65, cy - r * 0.65, cx + r * 0.65, cy + r * 0.65], fill=mid)
    draw.ellipse([cx - r * 0.32, cy - r * 0.32, cx + r * 0.32, cy + r * 0.32], fill=core)


def smoke(draw, cx, cy, r, col=(120, 120, 118)):
    for dx, dy, rr in [(-r * 0.5, -r * 0.3, r * 0.55), (0, -r * 0.7, r * 0.6),
                       (r * 0.5, -r * 0.4, r * 0.5), (r * 0.1, -r * 1.1, r * 0.45)]:
        draw.ellipse([cx + dx - rr, cy + dy - rr, cx + dx + rr, cy + dy + rr], fill=col)


# ---------------------------------------------------------------- map data
N_AMERICA = [(-168, 66), (-155, 71), (-140, 70), (-128, 71), (-115, 73), (-100, 73),
             (-95, 80), (-85, 76), (-80, 73), (-70, 70), (-65, 62), (-60, 55),
             (-55, 47), (-60, 45), (-65, 44), (-70, 42), (-75, 38), (-80, 32),
             (-81, 26), (-84, 30), (-90, 21), (-92, 15), (-95, 16), (-100, 18),
             (-105, 20), (-110, 23), (-114, 28), (-120, 34), (-124, 40), (-124, 48),
             (-130, 55), (-140, 60), (-150, 60), (-158, 58), (-165, 60)]
GREENLAND = [(-55, 60), (-45, 60), (-40, 65), (-30, 68), (-22, 70), (-20, 74),
             (-30, 76), (-45, 76), (-58, 74), (-58, 68)]
S_AMERICA = [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18),
             (-70, -23), (-70, -30), (-72, -37), (-73, -45), (-70, -52), (-66, -55),
             (-68, -50), (-65, -45), (-62, -40), (-58, -35), (-52, -32), (-48, -27),
             (-41, -22), (-39, -17), (-35, -9), (-35, -6), (-40, -3), (-44, -2),
             (-50, 0), (-53, 4), (-58, 6), (-62, 9), (-68, 11), (-72, 12), (-76, 10)]
AFRICA = [(-6, 35), (-10, 31), (-15, 27), (-17, 21), (-17, 15), (-15, 11),
          (-12, 8), (-8, 5), (-4, 5), (0, 6), (6, 4), (9, 4), (12, -1),
          (13, -5), (12, -10), (13, -15), (12, -18), (14, -22), (16, -28),
          (18, -32), (20, -35), (25, -34), (28, -32), (32, -28), (35, -24),
          (36, -20), (40, -15), (40, -10), (42, -5), (44, -2), (46, 0),
          (48, 2), (50, 10), (51, 12), (48, 14), (44, 13), (42, 15),
          (40, 15), (38, 18), (37, 22), (35, 28), (33, 31), (30, 32),
          (25, 32), (20, 32), (15, 33), (10, 34), (5, 37), (0, 36)]
EURASIA = [(-10, 36), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (-2, 49), (0, 50),
           (2, 51), (5, 53), (8, 54), (8, 57), (10, 58), (12, 56), (18, 56),
           (21, 55), (24, 58), (26, 59), (28, 60), (30, 62), (32, 64), (35, 66),
           (40, 67), (44, 68), (48, 68), (52, 68), (55, 69), (60, 69), (66, 70),
           (70, 72), (75, 72), (80, 73), (85, 74), (90, 75), (95, 76), (100, 76),
           (105, 77), (110, 74), (115, 73), (120, 73), (125, 72), (130, 72),
           (135, 71), (140, 71), (145, 72), (150, 71), (155, 70), (160, 70),
           (165, 69), (170, 67), (178, 66), (178, 64), (172, 62), (168, 60),
           (162, 58), (160, 55), (156, 51), (152, 56), (150, 59), (145, 59),
           (142, 56), (140, 52), (138, 48), (136, 45), (132, 43), (130, 42),
           (128, 38), (127, 35), (126, 38), (124, 39), (122, 38), (120, 34),
           (119, 30), (117, 26), (114, 22), (110, 20), (108, 17), (106, 12),
           (105, 9), (103, 7), (101, 6), (99, 8), (98, 12), (97, 16), (95, 16),
           (93, 18), (92, 21), (90, 22), (89, 22), (87, 21), (85, 19), (83, 17),
           (81, 15), (80, 13), (79, 9), (77, 8), (75, 12), (73, 17), (71, 21),
           (69, 22), (66, 25), (63, 25), (61, 25), (58, 25), (57, 26), (55, 26),
           (53, 26), (51, 27), (50, 29), (48, 30), (46, 29), (44, 29), (42, 27),
           (40, 26), (38, 24), (37, 22), (36, 20), (35, 18), (34, 16), (33, 15),
           (35, 13), (38, 14), (41, 15), (43, 12), (45, 12), (48, 14), (52, 15),
           (56, 17), (59, 22), (57, 25), (55, 26), (52, 26), (50, 28), (48, 29),
           (45, 28), (43, 27), (41, 28), (39, 28), (37, 29), (36, 30), (34, 31),
           (32, 31), (30, 33), (28, 34), (26, 35), (23, 36), (20, 36), (16, 38),
           (12, 38), (10, 37), (8, 37), (5, 37), (0, 36), (-5, 36), (-8, 35)]
UK = [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51), (-3, 50)]
JAPAN = [(130, 31), (132, 33), (135, 34), (137, 35), (139, 37), (140, 39),
         (141, 41), (142, 44), (144, 44), (143, 42), (141, 39), (140, 36),
         (138, 35), (135, 33), (131, 33)]
SUMATRA = [(95, 5), (98, 3), (101, 0), (104, -3), (106, -6), (104, -6), (100, -2), (97, 2)]
BORNEO = [(109, 1), (112, 3), (116, 6), (118, 2), (117, -2), (114, -4), (110, -3)]
NEW_GUINEA = [(131, -1), (136, -2), (141, -3), (146, -6), (150, -9), (147, -9),
              (142, -8), (137, -6), (132, -4)]
AUSTRALIA = [(114, -22), (114, -30), (116, -35), (120, -34), (124, -33), (129, -32),
             (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
             (153, -32), (153, -27), (150, -23), (146, -19), (142, -15), (142, -11),
             (137, -12), (135, -12), (132, -11), (130, -13), (126, -14), (122, -17),
             (118, -20)]
NEW_ZEALAND = [(167, -45), (170, -43), (173, -41), (175, -38), (177, -38),
               (174, -41), (172, -43), (169, -46)]
MADAGASCAR = [(44, -16), (47, -15), (50, -16), (49, -20), (47, -24), (45, -25), (44, -20)]
LAND_POLYS = [N_AMERICA, GREENLAND, S_AMERICA, AFRICA, EURASIA, UK, JAPAN,
              SUMATRA, BORNEO, NEW_GUINEA, AUSTRALIA, NEW_ZEALAND, MADAGASCAR]


def on_land(lon, lat):
    inside = False
    for poly in LAND_POLYS:
        j = len(poly) - 1
        c = False
        for i, (xi, yi) in enumerate(poly):
            xj, yj = poly[j]
            if ((yi > lat) != (yj > lat)) and \
               (lon < (xj - xi) * (lat - yi) / (yj - yi) + xi):
                c = not c
            j = i
        inside = inside or c
    return inside


# ---------------------------------------------------------------- content
HEROES = [
    dict(num=1, tag="Reuters", kind="cop31",
         head="COP31 nears a deal as approval session opens",
         body="Final text tabled in the early hours; no fossil-fuel mention; "
              "power target 35% by 2035; $120bn goal dropped."),
    dict(num=2, tag="AP", kind="bahrain",
         head="Iran strikes US bases in Bahrain",
         body="Tehran claims two Patriot radars hit and one site ablaze, no "
              "casualties; Bahrain says most were intercepted."),
    dict(num=3, tag="AP", kind="ukraine",
         head="148 drones over Ukraine tonight",
         body="Kryvyi Rih: 2 killed, 60 hurt; 161 drones shot down; 3 "
              "missiles and 12 glide bombs in the barrage."),
]

PANELS = [
    dict(num=4, tag="Reuters", kind="ship",
         head="Russian ship still burning in Finnish waters",
         body="Russian cargo ship still burning off Finland; 16 crew evacuated."),
    dict(num=5, tag="SCMP", kind="vote",
         head="Hong Kong votes for its Election Committee",
         body="856 candidates chase 723 seats; turnout 89.81% by 13:00."),
    dict(num=6, tag="UKMTO", kind="tanker",
         head="Two tankers hit leaving Hormuz",
         body="Two tankers hit leaving the Strait; Torkel still burning at anchor."),
    dict(num=7, tag="Reuters", kind="cricket",
         head="Pant 128 as India declare 720/9, lead 352",
         body="Pant 128, Rahul 136; India declare 720/9, lead 352; NZ 105/2."),
    dict(num=8, tag="F1", kind="race",
         head="Verstappen wins the Las Vegas GP",
         body="Verstappen wins in Las Vegas — third win in four years; Norris 2nd, Piastri 3rd."),
    dict(num=9, tag="Al Jazeera", kind="gaza",
         head="Four killed as Gaza ceasefire frays",
         body="Four killed as the ceasefire frays; aid van hit; Hamas seeks emergency talks."),
    dict(num=10, tag="AP", kind="badge",
         head="Mexico captures \u2018El Chapo Isidro\u2019",
         body="Mexico arrests top-10 FBI fugitive \u2018El Chapo Isidro\u2019; 11 killed in violence."),
    dict(num=11, tag="RFE/RL", kind="bolt",
         head="Iran rations power to 2 hours a day",
         body="Power rationed to 2 hours a day as gas output lags demand."),
    dict(num=12, tag="Reuters", kind="fire",
         head="Power-plant fire kills four in Basra",
         body="Power-plant fire kills four, injures 35."),
    dict(num=13, tag="ESA", kind="space",
         head="BepiColombo enters orbit of Mercury",
         body="ESA craft enters orbit around Mercury; first photos sent back."),
]

ALSO_LEFT = [
    "Bayelsa boat capsizes, 24 dead",
    "Eisenkot invites Likud to coalition talks",
    "Sudan: MSF says 5,000 still missing in El-Fasher",
    "Wembanyama scores 50, grabs 19 boards",
    "Nvidia faces SEC probe; shares fall 14%",
    "Bolsonaro in ICU, stable",
    "Estonia to shut Russia border on 1 Dec",
    "South Korea education minister quits over exam leak",
    "China bans US phones, calls them \u201cmalicious\u201d",
    "Japan holds first live-fire drill with India",
    "Nepal PM lands in Delhi on first visit",
    "Marles rejects US report on AUKUS subs",
]
ALSO_RIGHT = [
    "EU\u2013Indonesia trade deal scraps 98.5% of tariffs",
    "Belgium air-traffic strike grounds Monday flights",
    "France seeks UN action over Myanmar",
    "Chinese bomber turns back 170 km from Manila",
    "Liverpool v Man Utd 16:30 GMT; Pochettino\u2019s first game",
    "Zverev v Alcaraz in ATP final, 17:00 GMT",
    "Saudi-led coalition downs 3 Houthi missiles",
    "Four nations press Israel over Gaza aid",
    "Australia chase 188 to beat England in first T20",
    "Drone hits five-storey block in Kyiv Oblast",
    "Bitcoin rebounds above $60,000, up 1.85%",
    "Pope Leo hosts lunch for 1,300 poor guests",
    "World court: Myanmar committed genocide of Rohingya",
]

# (lon, lat, badge dx, badge dy)
PINS = [
    (30.7, 36.9, 12, -13),    # 1 COP31 Antalya
    (50.6, 26.2, 13, 9),      # 2 Bahrain
    (33.4, 47.9, -13, -11),   # 3 Kryvyi Rih
    (23.0, 60.0, -14, -7),    # 4 Sparta II, off Finland
    (114.2, 22.3, 13, -11),   # 5 Hong Kong
    (56.5, 26.6, 13, -13),    # 6 Hormuz
    (77.1, 28.6, 11, -13),    # 7 Delhi cricket
    (-115.1, 36.2, -13, -11), # 8 Las Vegas
    (34.5, 31.5, -13, 11),    # 9 Gaza
    (-107.4, 25.8, 13, 11),   # 10 Sinaloa
    (51.4, 35.7, 11, -13),    # 11 Tehran
    (47.8, 30.5, -13, -13),   # 12 Basra
    (8.6, 49.9, 13, -11),     # 13 Darmstadt (ESA)
]

REGIONS = [("Europe", 9, (31, 80, 140)), ("Middle East", 8, (176, 30, 36)),
           ("Asia", 9, (200, 150, 60)), ("Americas", 5, (60, 130, 70)),
           ("Africa", 2, (150, 110, 40)), ("Oceania", 3, (90, 90, 150)),
           ("Global", 2, (110, 110, 110))]

DATE_CHECK = ("Every story here happened, or was first reported, on Sunday 22 "
              "November 2026 in at least one time zone. Tonight\u2019s barrage was "
              "148 drones \u2014 not Friday\u2019s 400. Left out as earlier news: Peru "
              "quake (Fri 20 Nov) \u00b7 missiles landing in Poland (19 Nov) \u00b7 "
              "Kerch Bridge strikes (earlier this week) \u00b7 Shenzhen summit "
              "(19 Nov) \u00b7 Voyager 1 (18 Nov) \u00b7 GTA VI launch (19 Nov) \u00b7 "
              "Anthropic IPO (19 Nov). Not yet happened when drawn: final COP31 "
              "approval (06:00 GMT session) \u00b7 ATP final (17:00 GMT) \u00b7 "
              "Liverpool v Man Utd (16:30 GMT).")


# ---------------------------------------------------------------- scenes
def scene(draw, kind, x, y, w, h):
    w, h = int(w), int(h)
    if kind == "cop31":
        vgrad(draw, (x, y, x + w, y + h), (28, 68, 88), (14, 38, 55))
        draw.rectangle([x + 18, y + 8, x + w - 18, y + 34], fill=(240, 235, 215))
        draw.text((x + w / 2, y + 21), "COP31  ANTALYA", font=font(F_SANS_B, 15),
                  fill=NAVY, anchor="mm")
        for i, c in enumerate([(176, 30, 36), (255, 255, 255), (31, 80, 140),
                               (200, 150, 60), (60, 130, 70), (150, 60, 120)]):
            fx = x + 24 + i * 16
            draw.rectangle([fx, y + 38, fx + 11, y + 48], fill=c)
        for r in range(3):
            ry = y + 54 + r * 8
            draw.rectangle([x + 12, ry, x + w - 12, ry + 5], fill=(90, 110, 125))
            for c in range(9):
                cx = x + 22 + c * 32
                draw.ellipse([cx - 3, ry - 5, cx + 3, ry + 1], fill=(230, 220, 195))
    elif kind == "bahrain":
        vgrad(draw, (x, y, x + w, y + h), (12, 22, 44), (30, 34, 58))
        for sx, sy in [(40, 12), (90, 22), (150, 9), (210, 20), (260, 12), (300, 24)]:
            draw.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(220, 220, 200))
        base = y + h
        for bx, bw, bh in [(0, 46, 34), (48, 34, 52), (84, 52, 30), (140, 30, 44),
                           (172, 44, 26), (218, 36, 50), (256, 42, 32), (300, 26, 40)]:
            draw.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(8, 10, 16))
            for wy in range(base - bh + 6, base - 4, 9):
                for wx in range(bx + 6, bx + bw - 4, 10):
                    if (wx + wy) % 20 == 0:
                        draw.rectangle([x + wx, wy, x + wx + 3, wy + 4], fill=(255, 210, 110))
        burst(draw, x + 105, y + 52, 15)
        smoke(draw, x + 105, y + 46, 11)
        burst(draw, x + 245, y + 44, 11)
        draw.line([x + 60, y + 18, x + 105, y + 44], fill=(255, 180, 80), width=2)
    elif kind == "ukraine":
        vgrad(draw, (x, y, x + w, y + h), (10, 18, 38), (24, 30, 52))
        for sx, sy in [(30, 10), (80, 20), (140, 8), (200, 18), (250, 10), (310, 22)]:
            draw.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(220, 220, 200))
        base = y + h
        for bx, bw, bh in [(0, 40, 26), (42, 30, 40), (74, 48, 22), (124, 34, 36),
                           (160, 44, 24), (206, 30, 42), (238, 46, 28), (286, 40, 34)]:
            draw.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(7, 9, 15))
        draw.polygon([(x + 60, base), (x + 150, y + 6), (x + 175, y + 6), (x + 110, base)],
                     fill=(120, 130, 150))
        burst(draw, x + 95, y + 46, 14)
        burst(draw, x + 230, y + 52, 12)
        smoke(draw, x + 230, y + 46, 10)
        for dx, dy in [(120, 26), (180, 18), (260, 24), (300, 14)]:
            draw.ellipse([x + dx - 2, y + dy - 2, x + dx + 2, y + dy + 2], fill=(255, 90, 70))
            draw.line([x + dx - 12, y + dy + 6, x + dx, y + dy], fill=(255, 120, 90), width=1)
    elif kind in ("ship", "tanker"):
        vgrad(draw, (x, y, x + w, y + h), (70, 110, 135), (30, 55, 80))
        draw.rectangle([x + 8, y + h - 16, x + w - 8, y + h - 6], fill=(40, 40, 44))
        draw.rectangle([x + w * 0.55, y + h - 28, x + w * 0.8, y + h - 16], fill=(200, 200, 195))
        if kind == "ship":
            smoke(draw, x + w * 0.68, y + h - 16, 6)
            burst(draw, x + w * 0.3, y + h - 20, 8)
        else:
            draw.rectangle([x + 14, y + h - 30, x + w - 14, y + h - 16], fill=(120, 60, 40))
            burst(draw, x + w * 0.75, y + h - 26, 8)
        for wx in range(0, w, 26):
            draw.arc([x + wx, y + h - 6, x + wx + 24, y + h + 4], 180, 360, fill=(160, 190, 205))
    elif kind == "vote":
        vgrad(draw, (x, y, x + w, y + h), (176, 30, 36), (120, 20, 26))
        draw.rectangle([x + w * 0.32, y + 12, x + w * 0.68, y + h - 8], fill=(245, 240, 225))
        draw.rectangle([x + w * 0.32, y + 12, x + w * 0.68, y + 20], fill=(40, 60, 90))
        draw.line([x + w * 0.4, y + 28, x + w * 0.48, y + h - 14, x + w * 0.64, y + 16],
                  fill=RED, width=3)
    elif kind == "cricket":
        vgrad(draw, (x, y, x + w, y + h), (60, 130, 70), (30, 80, 45))
        draw.ellipse([x + w - 30, y + 8, x + w - 12, y + 26], fill=(255, 255, 255))
        draw.ellipse([x + w - 27, y + 11, x + w - 15, y + 23], fill=(220, 60, 50))
        draw.line([x + 22, y + h - 8, x + w * 0.55, y + 12], fill=(210, 170, 110), width=5)
        draw.ellipse([x + w * 0.6, y + 14, x + w * 0.6 + 7, y + 21], fill=(200, 40, 30))
    elif kind == "race":
        vgrad(draw, (x, y, x + w, y + h), (20, 20, 26), (50, 50, 60))
        for i in range(8):
            c = (245, 245, 240) if i % 2 == 0 else (20, 20, 20)
            draw.rectangle([x + i * (w // 8), y + 6, x + (i + 1) * (w // 8), y + 16], fill=c)
        draw.rounded_rectangle([x + 18, y + 22, x + w - 18, y + h - 8], radius=5, fill=(200, 30, 36))
        draw.rectangle([x + w * 0.35, y + 14, x + w * 0.62, y + 24], fill=(180, 220, 240))
        draw.ellipse([x + 34, y + h - 14, x + 48, y + h - 2], fill=(15, 15, 15))
        draw.ellipse([x + w - 48, y + h - 14, x + w - 34, y + h - 2], fill=(15, 15, 15))
    elif kind == "gaza":
        vgrad(draw, (x, y, x + w, y + h), (210, 180, 140), (160, 130, 100))
        for bx, bw, bh in [(10, 34, 26), (48, 28, 34), (80, 36, 22), (120, 30, 30), (154, 32, 24)]:
            draw.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(120, 100, 80))
        smoke(draw, x + 62, y + h - 18, 6)
        burst(draw, x + 135, y + h - 30, 9)
    elif kind == "badge":
        vgrad(draw, (x, y, x + w, y + h), (40, 60, 90), (20, 32, 52))
        draw.ellipse([x + w / 2 - 13, y + 8, x + w / 2 + 13, y + 34], fill=GOLD)
        draw.text((x + w / 2, y + 21), "\u2605", font=font(F_SANS_B, 16),
                  fill=NAVY, anchor="mm")
        draw.polygon([(x + w / 2 - 8, y + 30), (x + w / 2 + 8, y + 30),
                      (x + w / 2 + 4, y + h - 4), (x + w / 2 - 4, y + h - 4)], fill=RED)
    elif kind == "bolt":
        vgrad(draw, (x, y, x + w, y + h), (50, 50, 58), (25, 25, 32))
        draw.polygon([(x + w * 0.55, y + 4), (x + w * 0.32, y + h * 0.55),
                      (x + w * 0.48, y + h * 0.55), (x + w * 0.42, y + h - 4),
                      (x + w * 0.68, y + h * 0.45), (x + w * 0.52, y + h * 0.45)],
                     fill=(255, 200, 60))
    elif kind == "fire":
        vgrad(draw, (x, y, x + w, y + h), (60, 60, 70), (30, 30, 38))
        draw.rectangle([x + 20, y + h - 22, x + w - 20, y + h - 8], fill=(90, 85, 80))
        draw.rectangle([x + 30, y + h - 34, x + 42, y + h - 22], fill=(110, 105, 100))
        burst(draw, x + w / 2, y + h - 18, 9)
        smoke(draw, x + w / 2, y + h - 14, 6)
    elif kind == "space":
        vgrad(draw, (x, y, x + w, y + h), (10, 14, 30), (30, 40, 66))
        for sx, sy in [(16, 8), (50, 16), (90, 6), (140, 14), (170, 8)]:
            draw.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(220, 220, 200))
        draw.ellipse([x + w - 52, y + 8, x + w - 16, y + 44], fill=(180, 160, 140))
        draw.ellipse([x + w - 46, y + 14, x + w - 34, y + 26], fill=(150, 130, 115))
        draw.line([x + 20, y + h - 10, x + 62, y + 18], fill=(200, 200, 190), width=2)
        draw.rectangle([x + 52, y + 12, x + 66, y + 26], fill=(220, 220, 210))
        draw.rectangle([x + 30, y + 26, x + 44, y + 30], fill=(150, 160, 200))


# ---------------------------------------------------------------- page
def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    M = 14
    X1 = W - M

    # masthead
    d.rectangle([M, 8, X1, 50], fill=RED)
    d.text((26, 29), "SUNDAY EDITION", font=font(F_SANS_B, 11), fill=(255, 255, 255), anchor="lm")
    d.text((W / 2, 29), "THE WORLD IN ONE DAY", font=font(F_SERIF, 29),
           fill=(255, 255, 255), anchor="mm")
    d.text((X1 - 26, 29), "38 STORIES", font=font(F_SANS_B, 11), fill=(255, 255, 255), anchor="rm")

    # title + standfirst
    d.text((W / 2, 82), "Sunday 22 November 2026", font=font(F_SERIF, 42), fill=INK, anchor="mm")
    d.text((W / 2, 110), "COP31 nears a deal  \u00b7  Iran strikes US bases in Bahrain  \u00b7  "
           "148 drones over Ukraine tonight", font=font(F_SANS, 14), fill=(60, 58, 50), anchor="mm")

    # ---- THE DAY IN NUMBERS (dark signature box)
    ny0, ny1 = 122, 190
    d.rectangle([M, ny0, X1, ny1], fill=NAVY)
    d.text((M + 12, ny0 + 9), "THE DAY IN NUMBERS", font=font(F_SANS_B, 12), fill=GOLD)
    d.line([(M + 12, ny0 + 26), (X1 - 12, ny0 + 26)], fill=(70, 95, 125), width=1)
    stats = [("148", "drones over Ukraine tonight"),
             ("720/9", "India declare, lead 352"),
             ("89.81%", "Hong Kong turnout"),
             ("$60,020", "Bitcoin, up 1.85%"),
             ("16", "Sparta II crew saved"),
             ("2", "US bases struck")]
    cell_w = (X1 - M) / 6
    for i, (num, cap) in enumerate(stats):
        cx = M + cell_w * i + cell_w / 2
        d.text((cx, ny0 + 45), num, font=font(F_SERIF, 25), fill=(255, 255, 255), anchor="mm")
        d.text((cx, ny0 + 62), cap, font=font(F_SANS, 10), fill=(190, 200, 210), anchor="mm")

    # ---- THE DAY IN UTC strip
    uy0 = 196
    d.text((M, uy0 + 6), "THE DAY IN UTC", font=font(F_SANS_B, 12), fill=RED)
    d.line([(M, uy0 + 24), (X1, uy0 + 24)], fill=(150, 140, 120), width=2)
    utc = [("SAT NIGHT", "Bahrain strikes reported"),
           ("03:00 GMT", "COP31 objections close"),
           ("06:00 GMT", "COP31 approval session"),
           ("13:00", "Hong Kong turnout 89.81%"),
           ("16:30 GMT", "Liverpool v Man Utd"),
           ("17:00 GMT", "ATP final: Zverev\u2013Alcaraz")]
    for i, (t, label) in enumerate(utc):
        cx = M + cell_w * i + cell_w / 2
        d.ellipse([cx - 5, uy0 + 19, cx + 5, uy0 + 29], fill=RED)
        d.text((cx, uy0 + 38), t, font=font(F_SANS_B, 11), fill=INK, anchor="mm")
        for ln, line in enumerate(wrap(d, label, font(F_SANS, 10), cell_w - 12)):
            d.text((cx, uy0 + 52 + ln * 12), line, font=font(F_SANS, 10),
                   fill=GREY, anchor="mm")

    # ---- hero row
    hy0, hy1 = 266, 404
    hw = (X1 - M - 16) / 3
    for i, hero in enumerate(HEROES):
        hx = M + i * (hw + 8)
        d.rectangle([hx, hy0, hx + hw, hy1], outline=(160, 150, 130), width=1, fill=PAPER)
        scene(d, hero["kind"], hx + 1, hy0 + 1, hw - 2, 66)
        d.ellipse([hx + 8, hy0 + 8, hx + 30, hy0 + 30], fill=RED)
        d.text((hx + 19, hy0 + 19), str(hero["num"]), font=font(F_SANS_B, 13),
               fill=(255, 255, 255), anchor="mm")
        d.rectangle([hx + hw - 62, hy0 + 8, hx + hw - 8, hy0 + 24], fill=(255, 255, 255))
        d.text((hx + hw - 35, hy0 + 16), hero["tag"], font=font(F_SANS_B, 9), fill=INK, anchor="mm")
        ty = hy0 + 74
        for ln, line in enumerate(wrap(d, hero["head"], font(F_SERIF, 16), hw - 16)):
            d.text((hx + 8, ty + ln * 19), line, font=font(F_SERIF, 16), fill=INK)
        by = ty + 19 * len(wrap(d, hero["head"], font(F_SERIF, 16), hw - 16)) + 3
        for ln, line in enumerate(wrap(d, hero["body"], font(F_SANS, 10), hw - 16)):
            d.text((hx + 8, by + ln * 12), line, font=font(F_SANS, 10), fill=(50, 48, 42))

    # ---- panel grid, two rows of five
    pw = (X1 - M - 4 * 7) / 5
    for row in range(2):
        py0 = 410 + row * 96
        py1 = py0 + 92
        for col in range(5):
            p = PANELS[row * 5 + col]
            px = M + col * (pw + 7)
            d.rectangle([px, py0, px + pw, py1], outline=(160, 150, 130), width=1, fill=PAPER)
            scene(d, p["kind"], px + 1, py0 + 1, pw - 2, 34)
            d.ellipse([px + 6, py0 + 6, px + 26, py0 + 26], fill=RED)
            d.text((px + 16, py0 + 16), str(p["num"]), font=font(F_SANS_B, 11),
                   fill=(255, 255, 255), anchor="mm")
            d.rectangle([px + pw - 56, py0 + 6, px + pw - 6, py0 + 20], fill=(255, 255, 255))
            d.text((px + pw - 31, py0 + 13), p["tag"], font=font(F_SANS_B, 8), fill=INK, anchor="mm")
            ty = py0 + 38
            head_lines = wrap(d, p["head"], font(F_SERIF, 12), pw - 12)
            for ln, line in enumerate(head_lines[:2]):
                d.text((px + 6, ty + ln * 13), line, font=font(F_SERIF, 12), fill=INK)
            by = ty + 13 * min(2, len(head_lines)) + 2
            for ln, line in enumerate(wrap(d, p["body"], font(F_SANS, 10), pw - 12)[:2]):
                d.text((px + 6, by + ln * 11), line, font=font(F_SANS, 10), fill=(50, 48, 42))

    # ---- map
    my0 = 600
    d.text((M, my0), "WHERE IT HAPPENED \u2014 PINS 1\u201313 MATCH THE STORIES ABOVE",
           font=font(F_SANS_B, 11), fill=INK)
    mx0, my1, mx1, my2 = M, my0 + 16, X1, my0 + 106
    d.rectangle([mx0, my1, mx1, my2], fill=SEA, outline=(150, 140, 120), width=1)
    lat_top, lat_bot = 78.0, -58.0

    def ll_to_xy(lon, lat):
        return (mx0 + (lon + 180) / 360 * (mx1 - mx0),
                my1 + (lat_top - lat) / (lat_top - lat_bot) * (my2 - my1))

    step = 7
    yy = my1 + 4
    while yy < my2 - 2:
        xx = mx0 + 4
        while xx < mx1 - 2:
            lon = -180 + (xx - mx0) / (mx1 - mx0) * 360
            lat = lat_top - (yy - my1) / (my2 - my1) * (lat_top - lat_bot)
            if on_land(lon, lat):
                d.ellipse([xx - 2, yy - 2, xx + 2, yy + 2], fill=LAND)
            xx += step
        yy += step
    for i, (lon, lat, dx, dy) in enumerate(PINS, start=1):
        px, py = ll_to_xy(lon, lat)
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED, outline=(255, 255, 255), width=1)
        bx, by = px + dx, py + dy
        d.line([(px, py), (bx, by)], fill=RED, width=1)
        d.ellipse([bx - 8, by - 8, bx + 8, by + 8], fill=RED, outline=(255, 255, 255), width=1)
        d.text((bx, by), str(i), font=font(F_SANS_B, 9), fill=(255, 255, 255), anchor="mm")

    # ---- ALSO 14-38
    ay0 = 718
    d.text((M, ay0), "ALSO ON SUNDAY 22 NOVEMBER \u2014 25 MORE STORIES",
           font=font(F_SANS_B, 13), fill=RED)
    d.line([(M, ay0 + 18), (X1, ay0 + 18)], fill=RED, width=1)
    col_w = (X1 - M - 20) / 2
    for col, items in enumerate([ALSO_LEFT, ALSO_RIGHT]):
        cx = M + col * (col_w + 20)
        for j, item in enumerate(items):
            n = 14 + j + (0 if col == 0 else len(ALSO_LEFT))
            yy = ay0 + 26 + j * 12
            d.text((cx, yy), f"{n}.", font=font(F_SANS_B, 11), fill=RED)
            d.text((cx + 26, yy), item, font=font(F_SANS, 11), fill=INK)

    # ---- region bar
    ry0 = 904
    d.text((M, ry0), "STORIES BY REGION \u2014 38 IN ALL", font=font(F_SANS_B, 11), fill=INK)
    bx0, bx1 = M, X1
    by0, by1 = ry0 + 16, ry0 + 30
    total = sum(v for _, v, _ in REGIONS)
    x = bx0
    for name, v, col in REGIONS:
        wseg = (bx1 - bx0) * v / total
        d.rectangle([x, by0, x + wseg, by1], fill=col)
        x += wseg
    d.rectangle([bx0, by0, bx1, by1], outline=INK, width=1)
    lx = M
    d.text((M, by1 + 4), "  ".join(f"{name} {v}" for name, v, _ in REGIONS),
           font=font(F_SANS, 10), fill=GREY)

    # ---- DATE CHECK
    dy0 = 950
    d.rectangle([M, dy0, X1, dy0 + 48], outline=RED, width=2, fill=(255, 250, 240))
    d.text((M + 10, dy0 + 4), "DATE CHECK \u2014 WHAT THIS PAGE LEAVES OUT",
           font=font(F_SANS_B, 11), fill=RED)
    dc_lines = wrap(d, DATE_CHECK, font(F_SANS, 10), X1 - M - 20)
    for ln, line in enumerate(dc_lines[:3]):
        d.text((M + 10, dy0 + 19 + ln * 11), line, font=font(F_SANS, 10), fill=INK)

    # ---- footer
    d.text((W / 2, 1011), "Every story here happened, or was first reported, on Sunday 22 November 2026.  "
           "HOW WE CHECKED: Reuters \u00b7 AP \u00b7 AFP \u00b7 Al Jazeera \u00b7 SCMP \u00b7 UKMTO \u00b7 ESA \u00b7 Vatican News.",
           font=font(F_SANS_B, 10), fill=INK, anchor="mm")
    return img


if __name__ == "__main__":
    out = build()
    out = out.convert("P", palette=Image.ADAPTIVE, colors=160).convert("RGB")
    out.save("entry.png", optimize=True)
    print("saved entry.png", out.size)
