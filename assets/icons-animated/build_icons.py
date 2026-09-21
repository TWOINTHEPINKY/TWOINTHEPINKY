#!/usr/bin/env python3
"""
Генератор АНИМИРОВАННЫХ SVG-иконок для tech stack и анимированных разделителей.

Как работает:
  - скачивает чистые логотипы с CDN simple-icons (jsdelivr)
  - оборачивает их в SVG с CSS-анимацией (spin / pulse / float / wiggle / bounce)
  - результат — папка icons/*.svg, которые можно вставлять в README через <img>

Добавить новую иконку:
  1. найди slug на https://simpleicons.org (например "svelte", "elixir", "unity")
  2. допиши строку в список ICONS ниже: (slug, имя, цвет, анимация)
  3. запусти:  python3 build_icons.py

Анимации: spin | spin-slow | pulse | float | wiggle | bounce
"""
import os, re, urllib.request, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(HERE, "icons")
os.makedirs(OUT, exist_ok=True)

# (slug на simpleicons.org, имя файла, цвет бренда, тип анимации)
ICONS = [
    ("javascript",       "javascript", "#F7DF1E", "wiggle"),
    ("typescript",       "typescript", "#3178C6", "pulse"),
    ("react",            "react",      "#61DAFB", "spin"),
    ("vuedotjs",         "vue",        "#4FC08D", "float"),
    ("nodedotjs",        "nodejs",     "#339933", "float"),
    ("python",           "python",     "#3776AB", "pulse"),
    ("go",               "go",         "#00ADD8", "bounce"),
    ("rust",             "rust",       "#DEA584", "pulse"),
    ("java",             "java",       "#ED8B00", "float"),
    ("spring",           "spring",     "#6DB33F", "pulse"),
    ("php",              "php",        "#777BB4", "wiggle"),
    ("docker",           "docker",     "#2496ED", "float"),
    ("kubernetes",       "kubernetes", "#326CE5", "spin-slow"),
    ("postgresql",       "postgresql", "#4169E1", "pulse"),
    ("mongodb",          "mongodb",    "#47A248", "float"),
    ("redis",            "redis",      "#FF4438", "pulse"),
    ("mysql",            "mysql",      "#4479A1", "wiggle"),
    ("nginx",            "nginx",      "#009639", "pulse"),
    ("git",              "git",        "#F05032", "wiggle"),
    ("github",           "github",     "#E6EDF3", "pulse"),
    ("linux",            "linux",      "#FCC624", "float"),
    ("html5",            "html5",      "#E34F26", "pulse"),
    ("css3",             "css3",       "#1572B6", "pulse"),
    ("tailwindcss",      "tailwind",   "#06B6D4", "float"),
    ("visualstudiocode", "vscode",     "#007ACC", "wiggle"),
    ("figma",            "figma",      "#F24E1E", "bounce"),
    ("amazonaws",        "aws",        "#FF9900", "float"),
    ("discord",          "discord",    "#5865F2", "bounce"),
    ("telegram",         "telegram",   "#26A5E4", "bounce"),
]

ANIM = {
    "spin":      "spin 5s linear infinite",
    "spin-slow": "spin 10s linear infinite",
    "pulse":     "pulse 2.2s ease-in-out infinite",
    "float":     "float 3s ease-in-out infinite",
    "wiggle":    "wiggle 2s ease-in-out infinite",
    "bounce":    "bounce 1.6s cubic-bezier(.28,.84,.42,1) infinite",
}

KEYFRAMES = """
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.14)}}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-3.5px)}}
@keyframes wiggle{0%,100%{transform:rotate(-7deg)}50%{transform:rotate(7deg)}}
@keyframes bounce{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}
@keyframes halo{0%,100%{opacity:.30;transform:scale(1)}50%{opacity:.65;transform:scale(1.1)}}
"""

TPL = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
<title>{name}</title>
<defs><radialGradient id="glow"><stop offset="0" stop-color="{color}" stop-opacity=".6"/><stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient></defs>
<style>{kf}
.halo{{animation:halo 2.6s ease-in-out infinite;transform-origin:32px 32px}}
.ico{{animation:{anim};transform-origin:12px 12px}}
</style>
<circle class="halo" cx="32" cy="32" r="26" fill="url(#glow)"/>
<g transform="translate(20,20)"><g class="ico">{paths}</g></g>
</svg>
"""

def fetch_paths(slug: str):
    url = f"https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/{slug}.svg"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    svg = urllib.request.urlopen(req, timeout=15).read().decode()
    ds = re.findall(r'<path[^>]*?\sd="([^"]+)"', svg)
    if not ds:
        raise RuntimeError(f"no path in {slug}")
    return "".join(f'<path d="{d}" fill="{FILL}"/>' for d in ds)

ok, fail = [], []
for slug, name, color, anim in ICONS:
    global FILL
    FILL = color
    try:
        paths = fetch_paths(slug)
        svg = TPL.format(name=name, color=color, kf=KEYFRAMES,
                         anim=ANIM[anim], paths=paths)
        with open(os.path.join(OUT, f"{name}.svg"), "w") as f:
            f.write(svg)
        ok.append(name)
    except Exception as e:
        fail.append((slug, str(e)[:60]))

print(f"✅ Сгенерировано: {len(ok)} иконок -> {OUT}")
print("   " + ", ".join(ok))
if fail:
    print(f"⚠️ Не удалось: {fail}")
