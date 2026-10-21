# SanjanaOS — Interactive Terminal

Blue/cyan interactive developer portfolio, inspired by a Linux terminal popup.

## Local preview
Open `index.html` in a browser. For a local web server, run `python -m http.server 8000` in this folder and visit http://localhost:8000.

## GitHub Pages
1. In your profile repository `SanjanaGadamsetty/SanjanaGadamsetty`, create a folder `terminal`.
2. Upload `index.html`, `style.css`, `terminal.js` inside `terminal/`.
3. Go to Settings → Pages, select **Deploy from a branch**, branch **main**, folder **/(root)**, and Save.
4. Visit `https://sanjanagadamsetty.github.io/SanjanaGadamsetty/terminal/` once Pages finishes deployment.
5. Add this to your profile README:

```md
[💠 Launch my interactive developer terminal](https://sanjanagadamsetty.github.io/SanjanaGadamsetty/terminal/)
```

The GitHub profile README itself cannot execute JavaScript, so the terminal is hosted separately on GitHub Pages. The existing README, SVG stats, and snake workflow remain untouched.

## Customization
Edit the `replies`, `groups`, and `profiles` objects in `terminal.js`. The `github` command uses the public GitHub API at runtime; other profile text is static. Links are only clickable when they appear as full URLs.

Commands: help, whoami, about, education, journey, neofetch, skills, stack, projects, experience, coding, github, opensource, achievements, art, now, goals, contact, clear, history, date, theme, sudo hire-me, coffee, fortune, matrix.
