
import os
import json
import urllib.request
from datetime import date, timedelta
from pathlib import Path

USERNAME = "SanjanaGadamsetty"
TOKEN = os.environ["GITHUB_TOKEN"]

query = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar {
        weeks {
          contributionDays {
            date
            contributionCount
          }
        }
      }
    }
  }
}
"""

today = date.today()
start = today - timedelta(days=30)

payload = json.dumps({
    "query": query,
    "variables": {
        "login": USERNAME,
        "from": start.isoformat() + "T00:00:00Z",
        "to": today.isoformat() + "T23:59:59Z"
    }
}).encode()

request = urllib.request.Request(
    "https://api.github.com/graphql",
    data=payload,
    headers={
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "User-Agent": "github-profile-activity-graph"
    }
)

with urllib.request.urlopen(request) as response:
    result = json.load(response)

if "errors" in result:
    raise RuntimeError(result["errors"])

weeks = result["data"]["user"]["contributionsCollection"][
    "contributionCalendar"
]["weeks"]

days = sorted(
    (day for week in weeks for day in week["contributionDays"]
     if start.isoformat() <= day["date"] <= today.isoformat()),
    key=lambda day: day["date"]
)

if not days:
    raise RuntimeError("No contribution data returned")

values = [day["contributionCount"] for day in days]
maximum = max(max(values), 1)

width, height = 1000, 340
left, right = 75, 950
top, bottom = 85, 270

def x_at(i):
    return left + i * (right - left) / max(len(values) - 1, 1)

def y_at(value):
    return bottom - value / maximum * (bottom - top)

points = " ".join(
    f"{x_at(i):.1f},{y_at(value):.1f}"
    for i, value in enumerate(values)
)

area = f"{left},{bottom} {points} {right},{bottom}"

grid = ""
for i in range(5):
    y = top + i * (bottom - top) / 4
    grid += (
        f'<line x1="{left}" y1="{y:.1f}" '
        f'x2="{right}" y2="{y:.1f}" '
        f'stroke="#24354D" stroke-width="1"/>'
    )

labels = ""
for i in range(0, len(days), 5):
    labels += (
        f'<text x="{x_at(i):.1f}" y="300" '
        f'fill="#A9B5C8" font-size="13" text-anchor="middle">'
        f'{days[i]["date"][5:]}</text>'
    )

svg = f"""<svg xmlns="http://www.w3.org/2000/svg"
viewBox="0 0 {width} {height}" role="img"
aria-label="GitHub contributions over the last 31 days">
<defs>
  <linearGradient id="goldFill" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#D8B76A" stop-opacity=".40"/>
    <stop offset="100%" stop-color="#D8B76A" stop-opacity="0"/>
  </linearGradient>
</defs>
<rect width="100%" height="100%" rx="18" fill="#101827"/>
<text x="75" y="45" fill="#F5E6C4"
font-size="23" font-family="Arial" font-weight="bold">
GitHub Activity • Last 31 Days
</text>
{grid}
<polygon points="{area}" fill="url(#goldFill)"/>
<polyline points="{points}" fill="none"
stroke="#D8B76A" stroke-width="4"
stroke-linejoin="round" stroke-linecap="round"/>
{labels}
<text x="950" y="45" fill="#D8B76A"
font-size="17" text-anchor="end" font-family="Arial">
{sum(values)} contributions
</text>
</svg>"""

Path("activity-line-graph.svg").write_text(svg, encoding="utf-8")
print("Generated activity-line-graph.svg")
