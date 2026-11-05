
from pathlib import Path
from html import escape

platforms = [
    ("LeetCode", "DSA & Problem Solving"),
    ("GeeksforGeeks", "Data Structures & Algorithms"),
    ("CodeChef", "Competitive Programming"),
    ("HackerRank", "Coding Challenges"),
    ("Codeforces", "Contests & Ratings"),
    ("AtCoder", "Algorithm Contests"),
    ("HackerEarth", "Programming Challenges"),
]

W, H = 1000, 660

svg = [
    f'<svg xmlns="http://www.w3.org/2000/svg" '
    f'width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
    '<rect width="1000" height="660" rx="22" fill="#101827"/>',
    '<text x="500" y="62" text-anchor="middle" '
    'font-family="Arial" font-size="30" font-weight="bold" '
    'fill="#D8B76A">THE CODING ARENA</text>',
    '<text x="500" y="94" text-anchor="middle" '
    'font-family="Arial" font-size="15" '
    'fill="#A9B5C8">Seven Platforms · One Coding Journey</text>',
]

for i, (name, focus) in enumerate(platforms):
    col = i % 2
    row = i // 2
    x = 40 + col * 470
    y = 130 + row * 112

    svg.extend([
        f'<rect x="{x}" y="{y}" width="450" height="94" '
        'rx="14" fill="#192538" stroke="#53647B"/>',
        f'<text x="{x+22}" y="{y+37}" '
        'font-family="Arial" font-size="22" '
        f'font-weight="bold" fill="#D8B76A">{escape(name)}</text>',
        f'<text x="{x+22}" y="{y+65}" '
        'font-family="Arial" font-size="15" '
        f'fill="#A9B5C8">{escape(focus)}</text>',
    ])

svg.extend([
    '<line x1="40" y1="594" x2="960" y2="594" '
    'stroke="#53647B"/>',
    '<text x="500" y="625" text-anchor="middle" '
    'font-family="Arial" font-size="16" '
    'fill="#F5E6C4">Live statistics coming next</text>',
    '</svg>',
])

Path("coding-arena.svg").write_text(
    "\n".join(svg), encoding="utf-8"
)

print("Generated coding-arena.svg")
