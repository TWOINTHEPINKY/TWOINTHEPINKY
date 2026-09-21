#!/usr/bin/env python3
"""
Генератор текстовых эффектов (text-fx) для README:
  1. info-typewriter.svg   — абзац печатается построчно, с курсором и
                             переливающейся подсветкой слова "incredible"
  2. title-info.svg        — неоновый заголовок "info:" с мерцанием и курсором
  3. title-tech-stack.svg  — неоновый заголовок "tech stack:"

Текст НЕ меняется — меняется только подача. Анимации на SMIL/CSS внутри SVG:
на GitHub они работают через <img> (так же, как readme-typing-svg и capsule-render).

Перезапуск после правок текста:  python3 build_text_fx.py
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
os.makedirs(HERE, exist_ok=True)

# ════════════════ 1. TYPEWRITER-КАРТОЧКА С АБЗАЦЕМ ════════════════
# Строки — это ТОТ ЖЕ текст, просто разбитый на строки.
# Формат: [(фрагмент, стиль), ...]  стиль None = обычный, "hl" = подсветка
LINES = [
    [("I develop absolutely ", None), ("incredible", "hl"), (" things—specifically, creative", None)],
    [("projects. My work covers everything from frontend and backend", None)],
    [("development to integrating your custom bots and scripts. If you", None)],
    [("are familiar with my projects—or if something you’ve just seen", None)],
    [("caught your eye—and you have an idea, please get in touch.", None)],
    [("Contact me via the links below.", None)],
]

W, H = 620, 196          # размер карточки
TX = 30                  # x текста
CH = 7.62                # средняя ширина символа, px
FIRST, STEP = 56, 24     # baseline первой строки и шаг
T = 17.0                 # полный цикл анимации, сек
STARTS = [0.6, 3.3, 6.0, 8.7, 11.4, 13.9]
ENDS   = [3.0, 5.7, 8.4, 11.1, 13.6, 15.2]
FADE   = 16.2

def kt(t):  # время -> keyTime (0..1)
    return f"{min(max(t / T, 0.0), 1.0):.4f}"

# ── clip-маски (постепенное «написание» каждой строки) ──
clips, texts = [], []
for i, parts in enumerate(LINES):
    chars = sum(len(p) for p, _ in parts)
    cw = min(chars * CH * 1.12 + 8, 575)          # ширина раскрытия (с запасом)
    y_top = FIRST + i * STEP - 18
    clips.append(
        f'<clipPath id="c{i}"><rect x="{TX-4}" y="{y_top}" height="26" width="0">'
        f'<animate attributeName="width" values="0;0;{cw:.0f};{cw:.0f};0" '
        f'keyTimes="0;{kt(STARTS[i])};{kt(ENDS[i])};0.99;1" dur="{T}s" '
        f'repeatCount="indefinite"/></rect></clipPath>'
    )
    tspans = ""
    for txt, st in parts:
        esc = txt.replace("&", "&amp;").replace("<", "&lt;")
        if st == "hl":
            tspans += f'<tspan font-weight="700" fill="url(#hlGrad)">{esc}</tspan>'
        else:
            tspans += f'<tspan>{esc}</tspan>'
    texts.append(
        f'<text x="{TX}" y="{FIRST + i*STEP}" clip-path="url(#c{i})">{tspans}</text>'
    )

# ── траектория курсора (x и y по ключевым точкам) ──
xs, ys = [(0.0, TX)], [(0.0, FIRST - 15)]
for i in range(len(LINES)):
    s, e = STARTS[i], ENDS[i]
    ytop = FIRST + i * STEP - 15
    chars = sum(len(p) for p, _ in LINES[i])
    if i > 0:                                     # мгновенный прыжок на новую строку
        xs.append((s - 0.01, xs[-1][1]))
        ys.append((s - 0.01, ys[-1][1]))
    xs += [(s, TX), (e, TX + chars * CH)]
    ys += [(s, ytop), (e, ytop)]
xs += [(FADE, xs[-1][1]), (T, xs[-1][1])]
ys += [(FADE, ys[-1][1]), (T, ys[-1][1])]

def anim_points(pts, attr):
    vals = ";".join(f"{v:.1f}" for _, v in pts)
    times = ";".join(kt(t) for t, _ in pts)
    return f'<animate attributeName="{attr}" values="{vals}" keyTimes="{times}" dur="{T}s" repeatCount="indefinite"/>'

typewriter = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<!-- ✍️ Абзац «печатается» построчно. Текст тот же — изменилась только подача.
     Пересобрать после правок: python3 build_text_fx.py -->
<defs>
<linearGradient id="hlGrad" x1="-0.6" y1="0" x2="0.0" y2="0">
<stop offset="0" stop-color="#ff4dcd"/>
<stop offset=".5" stop-color="#eaffff"/>
<stop offset="1" stop-color="#00d4ff"/>
<animate attributeName="x1" values="-0.6;1.0" dur="2.4s" repeatCount="indefinite"/>
<animate attributeName="x2" values="0.0;1.6" dur="2.4s" repeatCount="indefinite"/>
</linearGradient>
<linearGradient id="accent" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#00d4ff"/><stop offset="1" stop-color="#ff4dcd"/>
</linearGradient>
</defs>
<style>
text{{font-family:'Segoe UI',Helvetica,Arial,sans-serif;font-size:15px;fill:#c9d1d9}}
</style>
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="#0d1117" stroke="#30363d"/>
<circle cx="24" cy="20" r="5.5" fill="#ff5f56"/><circle cx="42" cy="20" r="5.5" fill="#ffbd2e"/><circle cx="60" cy="20" r="5.5" fill="#27c93f"/>
<rect x="14" y="42" width="3" height="136" rx="1.5" fill="url(#accent)" opacity=".75"/>
<g>
<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.03;{kt(FADE)};0.995;1" dur="{T}s" repeatCount="indefinite"/>
{''.join(texts)}
<rect x="{TX}" y="{FIRST-15}" width="2.5" height="17" fill="#00d4ff">
{anim_points(xs, 'x')}
{anim_points(ys, 'y')}
<animate attributeName="opacity" values="1;0" keyTimes="0;0.5" calcMode="discrete" dur="0.85s" repeatCount="indefinite"/>
</rect>
</g>
<defs>{''.join(clips)}</defs>
</svg>'''

# ════════════════ 2. НЕОНОВЫЕ ЗАГОЛОВКИ ════════════════
def make_title(text, vb_w, c1, c2, font_px=30):
    char_w = font_px * 0.602                       # моноширинный
    text_w = len(text) * char_w
    cursor_x = 12 + text_w + 6
    glow_id, grad_id = "g", "s"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vb_w} 46" width="{vb_w}" height="46">
<defs>
<linearGradient id="{grad_id}" x1="-0.5" y1="0" x2="0.2" y2="0">
<stop offset="0" stop-color="{c1}"/><stop offset=".5" stop-color="#ffffff"/><stop offset="1" stop-color="{c2}"/>
<animate attributeName="x1" values="-0.5;1.0" dur="3s" repeatCount="indefinite"/>
<animate attributeName="x2" values="0.2;1.7" dur="3s" repeatCount="indefinite"/>
</linearGradient>
<filter id="{glow_id}" x="-40%" y="-60%" width="180%" height="220%"><feGaussianBlur stdDeviation="3"/></filter>
</defs>
<style>t{{font-family:'Fira Code',Consolas,Menlo,monospace;font-size:{font_px}px;font-weight:700}}</style>
<text class="t" x="12" y="31" fill="{c2}" filter="url(#{glow_id})" opacity=".45">
<animate attributeName="opacity" values=".25;.65;.25" dur="2.2s" repeatCount="indefinite"/>{text}</text>
<text class="t" x="12" y="31" fill="url(#{grad_id})">{text}</text>
<rect x="{cursor_x:.0f}" y="10" width="3" height="24" fill="{c2}">
<animate attributeName="opacity" values="1;0" keyTimes="0;0.5" calcMode="discrete" dur="0.9s" repeatCount="indefinite"/>
</rect>
</svg>'''

title_info = make_title("info:", 150, "#7b2ff7", "#00d4ff")
title_tech = make_title("tech stack:", 290, "#ff4dcd", "#7b2ff7")

for name, content in [
    ("info-typewriter.svg", typewriter),
    ("title-info.svg", title_info),
    ("title-tech-stack.svg", title_tech),
]:
    open(os.path.join(HERE, name), "w").write(content)
    print(f"✓ {name} ({len(content)//1024 or 1} KB)")

# ── валидация XML ──
import xml.dom.minidom
for name in ["info-typewriter.svg", "title-info.svg", "title-tech-stack.svg"]:
    xml.dom.minidom.parse(os.path.join(HERE, name))
print("✓ XML валиден")
