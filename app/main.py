

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

