from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from . import writing


app = FastAPI()
app.include_router(writing.router)


@app.get("/", response_class=RedirectResponse)
def index():
    return RedirectResponse(url="/writing/index")
