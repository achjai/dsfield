from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app=FastAPI()

templates=Jinja2Templates(directory="templates")

context_dict = {"page_title":"dsfield · learn data structures by hand", "anchorlist":["algorithms","arrays","about"]}
@app.get("/")
def home(request : Request):
    return templates.TemplateResponse(request,"home.html",context_dict)


context_algo={"algorithms":[{"slug":"bubble-sort","title":"Bubble sort", "description":"Description for bubble sort","status":"wip"},{"slug":"binary-search","title":"Binary search","description":"Description for binary search","status":"wip"}]}
@app.get("/algorithms")
def algorithm_page(request: Request):
    return templates.TemplateResponse(request, "algolist.html",context_algo)

@app.get("/algorithms/{topic}")
def topic(topic: str):
    pass

@app.get("/search")
def search(query:str):
    pass
