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
