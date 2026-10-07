# dsfield Learning Log

This file is my diary of what I did and what I learnt. I am learning with Claude (an AI assistant) as a tutor, so some of these notes were drafted with its help from my own code and questions. I write the code myself, and I use Claude to explain concepts and review my work.

---

## 30 September 2026

1. Installed FastAPI with `pip install "fastapi[standard]"`. The `[standard]` part also installs uvicorn (the server that actually runs the app) and the `fastapi` command line tool.
2. Created `app/main.py`.
3. Wrote my first route, which returns a small piece of JSON.
4. Ran it with `fastapi dev app/main.py`.
5. Opened `http://127.0.0.1:8000` in the browser and saw the JSON come back.

### How to run the app

From the project root (the folder that contains `app/`):

```bash
fastapi dev app/main.py
```

`dev` mode has auto reload, so when I save the file the server restarts by itself. This is only for development. Later, for real deployment, it would be `fastapi run`.

FastAPI also builds a free interactive page at `http://127.0.0.1:8000/docs` where I can see every route and test it with a button. Very useful for checking that a route works before I connect the frontend.

### My code

```python
from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def home():
    return {"message": "Hello, World!"}
```

---

## What is FastAPI and why use it

**FastAPI is a Python framework for building web APIs.**

A framework is a set of ready-made tools that handle the boring hard parts, so I only write the parts specific to my project. Without a framework, I would have to write code to open a network connection, read raw text sent by the browser, figure out which URL it wants, build a correctly formatted reply, and send it back. FastAPI does all of that for me. I just write normal Python functions and tell FastAPI which URL each one belongs to.

**An API** (Application Programming Interface) here means: a set of URLs that a program can call to get data or make something happen. My browser page will be one program, and my Python code will be another. The API is the way they talk.

**Why FastAPI specifically:**

- **Simple to write.** A working route is only a few lines, as seen above.
- **Fast.** It is one of the quickest Python frameworks, and it supports async code (I will learn this later).
- **Automatic docs.** The `/docs` page is generated from my code without any extra work.
- **Automatic validation.** Using Python type hints and Pydantic, it can check that incoming data is the right shape (for example, that a list of numbers really contains numbers) and send a clear error if it is not. This will matter a lot for dsfield, because users will type their own arrays.
- **Editor friendly.** Because it uses type hints, VS Code can autocomplete and warn me about mistakes.

**Why it fits dsfield:** the algorithms (bubble sort, binary search, and so on) will run in Python. The browser cannot call a Python function directly, so it sends a request to FastAPI, FastAPI runs the Python function, and the result goes back to the browser to be drawn.

---

## Web basics I needed to understand first

### Client and server

- The **client** is the thing that asks. Here it is the browser.
- The **server** is the thing that answers. Here it is my FastAPI app running on my own computer.
- `127.0.0.1` (also called `localhost`) means "this same computer". `8000` is the port, like a door number that my app is listening on.

### Request and response

Everything on the web is a conversation of two messages:

1. The client sends a **request**: "I want this URL, using this method."
2. The server sends a **response**: a status code, some headers, and a body.

The status code tells the result. `200` means OK. `404` means that URL does not exist. `422` means the data I sent was the wrong shape. `500` means the server code crashed.

### What is GET

**HTTP methods** describe what the client wants to do. The main ones:

- **GET**: "give me data." It should only read, never change anything. This is what the browser does whenever I type a URL and press Enter.
- **POST**: "here is some data, please process or store it." I will use this later to send a user's custom array to the server.
- **PUT / PATCH**: update something that exists.
- **DELETE**: remove something.

My route uses GET because it only reads and returns a message.

### What is JSON

**JSON** (JavaScript Object Notation) is a plain text format for sending structured data. It is the common language between my Python backend and the JavaScript frontend, because almost every language can read and write it.

The response from my route looks like this:

```json
{"message": "Hello, World!"}
```

Rules of JSON:

- Curly braces `{}` hold an object, which is a set of `"key": value` pairs.
- Square brackets `[]` hold a list, like `[5, 2, 4]`.
- Keys and strings must use **double quotes**. Single quotes are not valid JSON.
- Values can be strings, numbers, `true`, `false`, `null`, lists, or other objects.

Python and JSON look very similar but are not identical:

| Python | JSON |
|--------|------|
| dict | object |
| list | array |
| `True` / `False` | `true` / `false` |
| `None` | `null` |
| single or double quotes | double quotes only |

Important idea: a Python dict is a real object living in memory. JSON is just **text** that describes data. To send data over the network it has to be turned into text (this is called serialization), and the receiver turns it back into real objects. FastAPI does this conversion for me automatically.

---

## Line by line: what my code does

### Line 1: `from fastapi import FastAPI`

This loads the `FastAPI` **class** from the installed `fastapi` package so I can use it in my file. A class is a blueprint for making objects. `FastAPI` is the blueprint for "a web application".

### Line 3: `app=FastAPI()`

This creates an **object** (an instance) from that blueprint and stores it in a variable called `app`.

Think of `app` as the whole web application. It holds a list of all my routes (URL and function pairs) and all the settings. Every route I make later gets attached to this one object.

Two things to remember:

- The name `app` is only a convention, but it is what `fastapi dev` looks for by default, so I should keep it.
- The parentheses `()` are what actually create the object. `FastAPI` alone is the blueprint, `FastAPI()` builds one from it.

### Line 5: `@app.get("/")`

This is the most confusing line, so here it is in pieces.

**The `@` symbol** starts a **decorator**. A decorator is a way to attach extra behavior to a function by writing one line right above it.

To understand it, remember that in Python a function is just a value, like a number or a string. I can pass a function into another function as an argument. A decorator uses that idea. This:

```python
@app.get("/")
def home():
    ...
```

is a shorter way of writing:

```python
def home():
    ...
home=app.get("/")(home)
```

So `app.get("/")` is called first and it returns a function. Then that returned function is called with my `home` function as its argument.

**What it actually does here:** it **registers** my function in the app's routing table. It is like writing an entry in a phone book:

> When a **GET** request arrives for the path **`/`**, call the function **`home`**.

Breaking down the parts:

- `app` is the object I created.
- `.get` says this route answers **GET** requests. There is also `.post`, `.put`, `.delete`, and so on.
- `"/"` is the **path**, the part of the URL after the domain. `/` is the root, so this route answers `http://127.0.0.1:8000/`. A route at `"/hello"` would answer `http://127.0.0.1:8000/hello`.

Without the decorator, `home` would just be a normal Python function that nothing on the web knows about. The decorator is what connects it to a URL.

### Line 6: `def home():`

This defines a normal Python function called `home`.

- **The name** is my choice. FastAPI does not care what it is called. `home` is just readable.
- **No parameters** inside the parentheses, because this route needs no input from the user. Later I can add parameters, and FastAPI will fill them from the URL or from the data the client sends.
- **I never call this function myself.** FastAPI calls it for me every time a matching request arrives. That is a big mindset shift: I write the function, the framework decides when to run it.

### Line 7: `return {"message": "Hello, World!"}`

I return a normal Python **dict** with one key, `"message"`, and one value, `"Hello, World!"`.

FastAPI takes whatever I return and does the following automatically:

1. Converts the dict into JSON text.
2. Sets the response header `Content-Type: application/json`, so the browser knows it is JSON and not a web page.
3. Sets the status code to `200 OK`.
4. Sends it back to the client.

That is why I can return a plain dict and the browser receives proper JSON.

---

## The full journey of one request

When I open `http://127.0.0.1:8000/` in the browser:

1. The browser sends a **GET** request for the path `/` to my computer, port 8000.
2. **uvicorn** (the server FastAPI runs on) receives the raw request.
3. FastAPI looks in its routing table for a **GET** route matching `/`.
4. It finds the entry made by `@app.get("/")` and calls `home()`.
5. `home()` returns the dict.
6. FastAPI turns the dict into JSON and builds the response with status 200.
7. The browser receives it and shows `{"message":"Hello, World!"}`.

---

## Things to remember and watch out for

- **Run from the project root.** Running from inside `app/` will break imports between my own modules later.
- **Quote the brackets in Git Bash.** Use `pip install "fastapi[standard]"`, otherwise the shell may misread the brackets.
- **Put `fastapi[standard]` in `requirements.txt`**, not just `fastapi`.
- **Path collision coming up.** Right now `/` returns JSON. Later `/` needs to serve `index.html`, and one path cannot do two jobs. Plan: move API routes under a prefix like `/api/...` and let `/` serve the page.
- **DevTools is my friend.** The Network tab in the browser shows every request, its status code, and its response.

---

## Questions to look up next

- What is the difference between `def` and `async def` in a FastAPI route?
- How do path parameters (`/items/5`) and query parameters (`/items?limit=5`) work?
- What is Pydantic and how does it validate incoming data?
- How do I serve an `index.html` file and static files (CSS and JS)?
- How does `fetch()` in JavaScript call my route?

## Next step

Serve `index.html` from FastAPI, add a button, and use `fetch()` to call an API route and show the response on the page. This connects the backend and frontend.



---

## 1 October 2026

1. Added a list of posts (a tiny fake database) to `app/main.py`.
2. Made a route that returns the whole list as JSON.
3. Made the same route answer on two different URLs by stacking two decorators.
4. Made a route with a **path parameter** (`/content/{id}`) that returns one post as an HTML page.
5. Learnt about `include_in_schema`, which hides a route from the auto generated docs.

I explored these on my own and with Claude explaining concepts. These notes were drafted with Claude's help from my code, so I should rewrite the parts I am unsure about in my own words.

### Final code for today

```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
app=FastAPI()

@app.get("/")
def home():
    return {"message": "Hello, World!"}

posts=[
    {"id": 1, "title": "Arrays", "content": "This is the content for arrays."},
    {"id": 2, "title": "Strings", "content": "This is the content for strings."},
]

@app.get("/content")
@app.get("/show")
def content():
    return posts

@app.get("/content/{id}", response_class=HTMLResponse)
def html_content(id: int):
    return f"<h1>{posts[id-1]['title']}</h1><p>{posts[id-1]['content']}</p>"
```

---

## The `posts` list: data living in memory

```python
posts=[
    {"id": 1, "title": "Arrays", "content": "This is the content for arrays."},
    {"id": 2, "title": "Strings", "content": "This is the content for strings."},
]
```

- This is a normal Python **list** that holds **dictionaries**. Each dictionary is one post, with the keys `id`, `title`, and `content`.
- It sits at the top level of the file (outside any function), so it is created once when the server starts, and every route can read it.
- It acts like a **fake database**. Real apps store data in a database, but a list is enough to practise with.
- Because it only lives in memory, it is **reset every time the server restarts**. If I changed it while the app was running, the change would be lost on restart.
- A list of dictionaries is exactly the shape JSON uses for "an array of objects", so converting it to JSON is trivial for FastAPI.

---

## Returning the list: `/content`

```python
@app.get("/content")
def content():
    return posts
```

- Same pattern as yesterday: the decorator registers the function for **GET** requests on the path `/content`.
- This time the function returns a **list**, not a dict. FastAPI turns it into a JSON array:

```json
[{"id":1,"title":"Arrays","content":"This is the content for arrays."},{"id":2,"title":"Strings","content":"This is the content for strings."}]
```

- Lesson: FastAPI can convert dicts, lists, strings, numbers and more into JSON automatically. I just return normal Python data.

---

## Stacking two decorators: one function, two URLs

```python
@app.get("/content")
@app.get("/show")
def content():
    return posts
```

Now **both** `/content` and `/show` run the same function and return the same data.

**Why this works:** a decorator takes a function, does something with it (here, registers it in the routing table), and then **gives the same function back**. Since it gives the function back, a second decorator can be applied on top of it.

**The order of events:** decorators are applied from the **bottom up**, the one closest to the `def` first:

1. `@app.get("/show")` registers `content` for `/show` and hands `content` back.
2. `@app.get("/content")` registers that same `content` for `/content` and hands it back.

So the routing table now has two entries pointing at one function.

**Why it is useful:** an alias or old URL can keep working without copying the function. This is also a good case for `include_in_schema` (see below), because the second URL is just a duplicate.

---

## Path parameters: `/content/{id}`

```python
@app.get("/content/{id}", response_class=HTMLResponse)
def html_content(id: int):
    ...
```

### What is a path parameter

A **path parameter** is a changing part inside the URL. In `/content/{id}`, the curly braces mean: "this part can be anything, and I want to receive it."

- `/content/1` gives `id` the value 1.
- `/content/2` gives `id` the value 2.

One route handles all of them, instead of writing a separate route for every post.

### How FastAPI passes it to my function

FastAPI matches the **name inside the braces** with the **name of a function parameter**. The path has `{id}`, and the function has `id`, so FastAPI hands the value over. If the names did not match, the value would not arrive.

### Why `id: int` matters

URLs are just text, so the `1` in `/content/1` arrives as the text `"1"`. The type hint `int` tells FastAPI two things:

1. **Convert** the text into a real integer.
2. **Validate** it. If it cannot be converted, FastAPI stops and sends back an error before my function even runs.

I tested `/content/abc`: it returned a **422 Unprocessable Entity** error with a JSON body explaining that `id` should be a valid integer. I wrote zero code for that. This is the automatic validation I mentioned in the FastAPI notes, and it will be very useful when users type their own arrays.

---

## Returning HTML: `response_class=HTMLResponse`

```python
from fastapi.responses import HTMLResponse
```

Every route has a **response class**, which decides how the returned value is packaged. The default is JSON. When I return HTML text, I need to say so.

- With `response_class=HTMLResponse`, the string I return is sent with the header `Content-Type: text/html`, so the **browser renders it as a real web page** (a big heading and a paragraph).
- Without it, FastAPI would treat my string as JSON, wrap it in quotes, and the browser would show the raw `<h1>` tags as plain text.
- It also changes the `/docs` page, which now shows this route as returning `text/html`.

---

## The f-string and the indexing

```python
return f"<h1>{posts[id-1]['title']}</h1><p>{posts[id-1]['content']}</p>"
```

**f-string:** a string with an `f` in front. Anything inside `{ }` is treated as Python code, evaluated, and inserted into the text. That is how the title and content end up inside the HTML tags.

**Reading `posts[id-1]['title']` from the inside out:**

1. `id-1` is a number. If `id` is 1, this is 0.
2. `posts[0]` takes the item at position 0 of the list, which is the first dictionary.
3. `['title']` takes the value stored under the key `title` in that dictionary.

**Why `id-1`:** Python lists start counting at **0**, but my post ids start at **1**. So post 1 is at position 0, post 2 is at position 1, and so on.

**Quotes:** the string is wrapped in double quotes, so I used single quotes inside (`['title']`). Mixing them avoids the quotes ending the string too early.

---

## Known limits of this code (things I noticed, to fix later)

This works for my two posts, but I learnt where it is fragile:

- **An id is a label, not a position.** `id-1` only works if ids are exactly 1, 2, 3 with no gaps and no reordering. If a post is removed or the order changes, the URL and the data would not match any more. A better way is to **search** the list for the post whose `"id"` equals the one requested.
- **`/content/0`** gives `posts[-1]`. In Python, a negative index counts from the end, so I get the last post, which is wrong.
- **`/content/99`** would crash with an `IndexError` and send a **500 Internal Server Error**. The right answer is a **404 Not Found**. FastAPI has `HTTPException` for this, which I should look up.
- **Building HTML with f-strings** is fine for practice, but dsfield should have its API return **JSON** and let the page's JavaScript draw it.
- **Security:** if text ever comes from users and is pasted into HTML like this, someone can inject scripts into the page. This is called **XSS** (cross site scripting). My data is hardcoded now, so it is safe, but I should remember it exists.

---

## `include_in_schema`: hiding a route from the docs

### What the schema is

FastAPI automatically builds a machine readable description of my whole API. It is called the **OpenAPI schema**, and it lives at `/openapi.json`. The pretty pages I use, **`/docs`** (Swagger UI) and **`/redoc`**, are both generated from it. So "in the schema" really means "shown in the docs".

### What `include_in_schema=False` does

It is an option I can put in a route decorator:

```python
@app.get("/show", include_in_schema=False)
def content():
    return posts
```

- The route **still works** normally. Visiting `/show` still returns the data.
- It just **disappears from `/docs`, `/redoc`, and `/openapi.json`**.

### When to use it

- **Duplicate or alias URLs.** Like `/show` in my code: it only repeats `/content`, so it only clutters the docs.
- **Routes that serve web pages**, like the one that will return `index.html` at `/`. The docs are meant to list the API, not the pages.
- **Internal or helper routes** such as health checks that I do not want to advertise.

### An important warning

Hiding a route is **not security**. It only hides it from the documentation. Anyone who knows or guesses the URL can still call it. Protecting a route needs authentication, which I will learn later when I add login.

### Where I stand

I have not added this to my code yet. `/show` currently appears in `/docs` as a separate entry, so `include_in_schema=False` on it would be a good thing to try next time and then compare the `/docs` page before and after.

---

## Quick reference of today's new ideas

| Idea | One line summary |
|------|------------------|
| In-memory list of dicts | A fake database that resets on restart |
| Returning a list | FastAPI converts it to a JSON array |
| Stacked decorators | One function can serve several URLs |
| Path parameter `{id}` | A changing part of the URL, passed into a function parameter of the same name |
| `id: int` | Converts text to a number and rejects bad input with a 422 |
| `response_class=HTMLResponse` | Sends the returned string as a real web page |
| f-string | Insert Python values into text with `{ }` |
| `include_in_schema=False` | Hides a route from the docs but it still works |

---

## In my own words (to fill in myself)

Write two or three sentences here without help, for example:

- What does a path parameter let me do that a fixed route cannot?
- Why can two decorators sit on top of one function?
- What would I change first in the `/content/{id}` route, and why?

## Questions to look up next

- How do I raise a 404 with `HTTPException` when an id is not found?
- How do query parameters (`/content?limit=1`) differ from path parameters?
- How do I search a list for a matching dictionary (a loop first, then `next()` with a generator expression)?
- What is Pydantic and how does it describe the shape of data?

## Next step

Still the same goal: move the API routes under a prefix like `/api`, serve `index.html` at `/`, and use `fetch()` in JavaScript to call the API and show the result on the page.
 

 ---

 ## 2 October 2026

Today the project went from routes that return data to a real homepage in the browser. I did not write the homepage myself: I asked Claude to draft the HTML, CSS and JavaScript for a landing page, saved it as `templates/home.html`, and then read through it and wired it into FastAPI. The FastAPI part in `app/main.py` is code I wrote and edited myself.

### What I did today

1. Asked Claude to draft a homepage for dsfield and saved it as `templates/home.html` (a new `templates/` folder at the project root, next to `app/`).
2. Set up `Jinja2Templates` in `app/main.py` and changed the `/` route to render that file.
3. Replaced the old JSON `Hello, World!` response at `/`. This also solves the "path collision" worry from day 1: `/` is now the page, not JSON.
4. Removed the `/content/{id}` HTML route and the `HTMLResponse` import from day 2. The `posts` list, `/content` and `/show` are still there.

### A change from my plan

On day 1 and day 2 the plan was: put a plain file at `static/index.html`, serve it with `FileResponse`, and move API routes under `/api`. Today I used a **template** in `templates/home.html` served through Jinja2 instead.

The reason for this choice: a template can receive data from Python later (for example a list of algorithms), and a plain static file cannot. The cost: the empty `static/index.html` from my first folder structure is now unused, so I need to decide whether to delete it. The `/api` prefix and `fetch()` steps have not been done yet.

### My code today

```python
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app=FastAPI()

templates=Jinja2Templates(directory="templates")

@app.get("/")
def home(request : Request):
    return templates.TemplateResponse(request,"home.html")

posts=[
    {"id": 1, "title": "Arrays", "content": "This is the content for arrays."},
    {"id": 2, "title": "Strings", "content": "This is the content for strings."},
]

@app.get("/content")
@app.get("/show")
def content():
    return posts
```

(This is with the unused `tempfile` line removed.)

---

## What is a template?

A **template** is an HTML file that a backend can fill in before sending it to the browser.

- A normal HTML file is the same every time.
- A template can have **placeholders**. Python supplies values, and the final page is built from the two together.

**Important honesty note:** my `home.html` has **no placeholders**, and my route passes **no data** to it. So right now it behaves exactly like a static page that happens to be sent through Jinja2. It becomes truly dynamic only when I pass data in and use it inside the HTML.

---

## What is Jinja2?

**Jinja2** is a Python **template engine**. It reads an HTML file, replaces its special markers with real values, and gives back the finished HTML.

Its markers look like this:

- `{{ something }}` prints a value
- `{% ... %}` is a statement, like a loop or an if
- `{# ... #}` is a comment

None of these are in my `home.html` yet.

**A lesson from this:** because Jinja2 treats `{{`, `{%` and `{#` as special, CSS and JavaScript written inside a template can occasionally clash with it. My file has CSS and JS inline, and it happens to be safe. Moving them into separate static files later avoids the problem.

It came with `fastapi[standard]`, so I did not have to install anything extra.

---

## What changed in `main.py`

### The `/` route, before and after

**Day 1:** `/` returned a dictionary, and FastAPI turned it into JSON.

```python
@app.get("/")
def home():
    return {"message": "Hello, World!"}
```

**Today:** `/` renders a file and the browser shows a real page.

```python
@app.get("/")
def home(request : Request):
    return templates.TemplateResponse(request,"home.html")
```

**Day 2 already returned HTML** from `/content/{id}`, but it built the HTML out of an f-string inside Python. What is new today is that the HTML lives in its **own file** and Python just points to it. That is much cleaner for anything longer than a couple of tags.

### The new pieces, one by one

- `from fastapi import FastAPI, Request`: I now import `Request` as well.
- `from fastapi.templating import Jinja2Templates`: the class that connects FastAPI to Jinja2.
- `templates=Jinja2Templates(directory="templates")`: creates a template loader and tells it which folder holds my HTML files. Like `app`, it is an **object** made from a class.
- `def home(request : Request):` : the type hint `Request` tells FastAPI "pass me the incoming request object itself". FastAPI treats a parameter annotated this way as the raw request, not as a value from the URL.
- `templates.TemplateResponse(request,"home.html")`: finds `home.html` in the templates folder, renders it, and returns it as the response. I used the newer form where `request` comes **first**. Older tutorials write `TemplateResponse("home.html", {"request": request})`, which still works but is the old style.

### Why the route needs `request`

The template engine receives the request too, so templates can use helpers that depend on it (for example, building URLs). My page does not use any of that yet, but the function needs to be written this way.

### Where the folder is looked up

`directory="templates"` is a **relative path**, so it is found from the folder where I run `fastapi dev`. This is the same reason I must run it from the **project root**. If I ran it from inside `app/`, FastAPI would look for `app/templates` and fail.

---

## What is inside `home.html` (Claude drafted it, I read through it)

**Head**
- Loads three fonts from **Google Fonts**: Instrument Serif (headings), Inter (body text) and JetBrains Mono (small labels). This needs an internet connection. Without it the page falls back to system fonts.
- All CSS is inside one `<style>` tag in the same file.

**CSS ideas worth knowing**
- **CSS variables** are defined once in `:root` (`--paper`, `--ink`, `--accent`, and so on) and reused everywhere. To change the whole colour scheme, I change a few lines at the top.
- **CSS grid** builds the two column hero and the three column cards.
- **Media queries** (at 940px and 600px) make the layout collapse to one column on small screens.
- A **sticky header** stays at the top while scrolling, with a blurred background.
- `prefers-reduced-motion` turns animations off for people who have asked their device for less motion.

**Page sections, top to bottom:** header with navigation, hero (headline, buttons, a live bubble sort panel), about cards, algorithms cards, an arrays section with an example step trace, a call to action box, and a footer.

**JavaScript (at the bottom, also inline)**
1. **Scroll reveal:** elements with the class `reveal` start hidden. An `IntersectionObserver` watches them and adds the class `in` when they scroll into view, which fades them in.
2. **Bubble sort animation in the hero panel:** it runs bubble sort once on a fixed array and **records every step** in a list (compare, swap, done). Then a loop plays the steps back one by one with timers, colouring the bars. It restarts after finishing and pauses when the browser tab is hidden.

**That second part is the same idea as my main plan:** generate the steps first, then play them back. The difference is that here the steps are made by JavaScript, and in the real dsfield they will be made by Python and sent as JSON.

---

## Things to fix or decide

- **The page says "runs in the browser".** The hero demo does, but my real plan is that Python runs the algorithms. I should reword that line so the page does not promise something different from how dsfield will work.
- **Buttons are placeholders.** "open app" and "start learning" link to `#` and go nowhere yet.
- **The hero demo uses a fixed array**, not the user's own input. The custom input feature still has to be built.
- **The empty `static/index.html`:** keep it or delete it?
- **CSS and JS are inline.** Later I should move them to `static/css` and `static/js` and serve them with `StaticFiles`.
- **`/` and the docs:** `/` is now a page route, which is exactly the case where `include_in_schema=False` makes sense (from day 2). I still need to check how `/` and `/show` look in `/docs` and decide whether to hide them.

---

## Quick reference

| Idea | One line summary |
|------|------------------|
| Template | An HTML file the backend can fill in |
| Jinja2 | The Python engine that fills templates |
| `Jinja2Templates(directory=...)` | Tells FastAPI where my HTML files are |
| `Request` parameter | FastAPI passes me the raw incoming request |
| `TemplateResponse(request,"home.html")` | Render the file and send it as the response |
| Relative `directory` | Found from where I run the app, so run from the project root |

---

## In my own words (to fill in myself)

- What is the difference between returning a dict and returning a `TemplateResponse`?
- Why does my homepage not need Jinja2 yet, and what would make it need it?
- What is one thing in `home.html` I understand, and one thing I do not?

## Questions to look up next

- How do I serve CSS and JS as static files with `StaticFiles`, and link them from the template?
- How do I pass data from Python into a template and print it with `{{ }}`?
- How do I send an array from the page to FastAPI with `fetch()` and a POST route?
- How do I return a bubble sort trace as JSON from Python?

## Next step

Build the first real feature: a route that takes a list of numbers and returns a bubble sort trace as JSON (full state per step), then call it from the page with `fetch()` and draw the steps.

---

## 4 October 2026

Today I made `home.html` receive data from Python. Until now it had no placeholders and `main.py` passed no data. Now the page title and the nav links come from `main.py`.

### What I did today

1. Made a **context dict** in `app/main.py` with two keys: `page_title` and `anchorlist`.
2. Passed it as the third argument of `TemplateResponse` in the `/` route.
3. Replaced the hardcoded `<title>` in `home.html` with `{{page_title}}`.
4. Replaced the hardcoded nav links in `home.html` with a **for loop** over `anchorlist`.

### My code today

`app/main.py`:

```python
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app=FastAPI()

templates=Jinja2Templates(directory="templates")

context_dict = {"page_title":"dsfield · learn data structures by hand", "anchorlist":["algorithms","arrays","about"]}
@app.get("/")
def home(request : Request):
    return templates.TemplateResponse(request,"home.html",context_dict)
```

`templates/home.html` (title and nav):

```html
<title>{{page_title}}</title>
...
{% for anchor in anchorlist %}
<a href="{{anchor}}">{{anchor}}</a>
{% endfor %}
```

---

## The context dict

- A normal Python dictionary, passed as the **third argument** of `TemplateResponse(request, "home.html", context_dict)`.
- It is the **only way** to get data from Python into a template. Jinja cannot see my Python variables, so anything the page needs has to be in this dict.
- The **keys become variable names** in the template. `"page_title"` in the dict is `{{page_title}}` in the HTML. The names must match **exactly**.
- It lives in `main.py`, not in `home.html`.

---

## The Jinja markers I used

| Marker | What it does |
|--------|--------------|
| `{{ x }}` | Prints a value into the page |
| `{% ... %}` | Logic such as a loop. Prints nothing by itself |

Everything outside the markers (all the CSS, JS and HTML in `home.html`) is copied to the output unchanged. That is why the page kept working before I added any placeholders.

---

## The for loop in the nav

- Jinja takes the chunk between `{% for %}` and `{% endfor %}` and **repeats it once per item** in `anchorlist`, with `anchor` set to the current item each time.
- Compared to Python: `{% for anchor in anchorlist %}` is `for anchor in anchorlist:`, and `{{anchor}}` is like a `print` that writes into the page.
- It needs `{% endfor %}` because HTML has no indentation, so Jinja can't tell where the repeated chunk ends.
- Benefit: to add a nav link I only add a string to the list in `main.py`. I don't touch the HTML.

---

## What the browser receives

Jinja runs on the **server**, once per request. The browser only gets the finished HTML. In the page source (Ctrl+U) there is no `{{ }}` or `{% %}`, just three plain `<a>` tags with the values filled in.

---

## Things to fix or watch

- **Bug in the nav links:** the anchors are `"algorithms"`, `"arrays"`, `"about"`, but the sections are linked with `#`. So `href="{{anchor}}"` outputs `href="algorithms"`, which tries to open a new page instead of scrolling to the section. Fix in the template only: put a `#` before the `{{ }}` in the href. Check by hovering a link and reading the URL at the bottom of the browser.
- **Wrong variable name = blank, no error.** If I misspell a key like `page_title` in the template, Jinja quietly renders nothing. If something is missing and there is no error, check the key names first.
- **Must load through the server.** Opening `home.html` directly in the browser shows no Jinja output. Use `127.0.0.1:8000`.
- **Order of the nav items** is the order of the list in `main.py` (algorithms, arrays, about). The sections on the page run about, algorithms, arrays, so I may want to reorder.

---

## Quick reference

| Idea | One line summary |
|------|------------------|
| Context dict | Python dict passed to the template; keys become variable names |
| `{{page_title}}` | Prints the title into `<title>` |
| `{% for anchor in anchorlist %}` | Repeats one `<a>` per list item |
| Server-side rendering | Jinja runs on the server; the browser only sees finished HTML |
| Silent failure | A wrong variable name renders as blank, not an error |

---

## In my own words (to fill in myself)

- Why can't `home.html` just read the variables in `main.py`, and what do I do instead?
- Why does the for loop need `endfor` when Python doesn't need an end marker?
- What would I change in `main.py` to add a fourth nav link, and what would I change in the HTML?

## Questions to look up next

- How do I loop over a list of dicts and read fields (like `post.title` from my `posts` list)?
- How do I show a message when a list is empty?
- How do I move the repeated nav and footer into a shared base template?

## Next step

Fix the `#` in the nav hrefs, then use the `posts` list in a template.

---

## 7 October 2026

Today I moved the shared page structure into a Jinja layout so the homepage and algorithms page can use the same shell.

### What I did today

1. Made `templates/layout.html` the base template, with the document head, site navigation, main content area, footer, and Jinja blocks for page-specific content and scripts.
2. Moved the homepage's shared fonts and CSS into `templates/shared_styles.html`, included by the layout so both pages use the same styling.
3. Changed `home.html` to extend `layout.html`. Its page content and bubble-sort JavaScript stay in their own blocks.
4. Changed `algolist.html` to extend `layout.html` too, and gave it its own page title.
5. Updated `/algorithms` in `app/main.py` to render `algolist.html` with the page context, including the nav links.
6. Removed an unused Flask import that stopped the FastAPI app from importing.

### The Jinja layout

```html
{% extends "layout.html" %}

{% block content %}
  <!-- page-specific content -->
{% endblock %}
```

`layout.html` contains the parts common to both pages. The child template fills in the named blocks, so the browser receives one complete HTML document without duplicating the shared header, footer, or styles.

### What I checked

I rendered both templates and checked that each output has one document, the shared styles, header, and footer. I also requested `/` and `/algorithms` through FastAPI's test client; both returned HTTP 200 with their expected page titles and shared layout.

### Next step

Build out the algorithms page with the list of available algorithms, then link each item to its own page.