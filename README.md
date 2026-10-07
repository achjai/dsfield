# dsfield

An interactive web app for learning data structures and algorithms visually. Instead of only watching prebuilt examples, you can enter your own input (for example, your own array or tree values) and step through what the algorithm does, with a plain-English explanation of the logic and intuition behind every step.

**Status:** early development, running locally. Arrays are the first topic. The homepage and an algorithms list page (with a search bar) are in place, built on a shared base layout. The algorithm detail pages, search, and the visualiser itself are still to come.

**How it works:** Python (FastAPI) runs the algorithm and returns a full step-by-step trace as JSON. The browser plays that trace back with SVG, with controls to step forward, step back, and change speed.

**Stack:** Python, FastAPI, Jinja2 templates, HTML, CSS, vanilla JavaScript (SVG)

**About this project:** a learning project. I am building it to learn Python, FastAPI, and how the web works, with Claude as a tutor. Progress is logged in [NOTES.md](NOTES.md).