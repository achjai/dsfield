from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates

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
def algorithm_page(request: Request):
    context = {
        **context_dict,
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
