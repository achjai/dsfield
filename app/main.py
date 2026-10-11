from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
import csv
from fastapi import Form
from fastapi.responses import RedirectResponse
app=FastAPI()

templates=Jinja2Templates(directory="templates")

context_dict = {"page_title":"dsfield · learn data structures by hand", "anchorlist":["algorithms","arrays","about"]}
@app.get("/")
def home(request : Request):
    return templates.TemplateResponse(request,"home.html",context_dict)

ALGORITHMS={
    "bubble-sort":{"title":"Bubble Sort","description":"Description for bubble sort","status":"wip"}, "binary-search":{"title":"Binary Search","description":"Description for binary search","status":"wip"}
}

@app.get("/algorithms")
def algorithm_page(request: Request, requested: int =0):
    context = {
        **context_dict, "requested":requested,
        "algorithms": [
            {"slug": slug, **algo}
            for slug, algo in ALGORITHMS.items()
        ],
    }
    return templates.TemplateResponse(request, "algolist.html", context)

@app.get("/algorithms/{topic}")
def algorithm_detailed(request: Request, topic: str):
    algo = ALGORITHMS.get(topic)
    if algo is None:
        raise HTTPException(status_code=404, detail="Algorithm not found")
    context = {**context_dict, "algo": {"slug": topic, **algo}}
    return templates.TemplateResponse(request, "algo.html", context)

@app.get("/search")
def search(request: Request, query: str):
    q = query.lower()
    matches = [
        {"slug": slug, **algo}
        for slug, algo in ALGORITHMS.items()
        if q in algo["title"].lower() or q in algo["description"].lower()
    ]
    context = {**context_dict, "algorithms": matches, "query": query}
    return templates.TemplateResponse(request, "algolist.html", context)

@app.get("/request-algorithm")
def algoReq(request : Request, query: str =''):
    context={**context_dict, "query":query}
    return templates.TemplateResponse(request, "request_algorithm.html",context)

@app.post("/request-algorithm")
def reqPost(algorithm:str=Form(...),details:str=Form("")):
    with open("algo_req.csv","a",newline="",encoding="utf-8") as f:
        csv.writer(f).writerow([algorithm,details])
    return RedirectResponse("/algorithms?requested=1",status_code=303)
    