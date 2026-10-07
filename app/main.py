from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app=FastAPI()

templates=Jinja2Templates(directory="templates")

context_dict = {"page_title":"dsfield · learn data structures by hand", "anchorlist":["algorithms","arrays","about"]}
@app.get("/")
def home(request : Request):
    return templates.TemplateResponse(request,"home.html",context_dict)



@app.get("/algorithms")
def topics(request: Request):
    return templates.TemplateResponse(request, "algolist.html", context_dict)

@app.get("/algorithms/{topic}")
def topic(topic: str):
    pass

@app.get("/search")
def search(query:str):
    pass
