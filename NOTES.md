# dsfield Learning Log

I am building dsfield to learn Python, FastAPI, and how the web actually works. This file is my diary of what I did and what I understood, written in my own words.

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