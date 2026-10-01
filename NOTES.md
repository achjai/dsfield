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
