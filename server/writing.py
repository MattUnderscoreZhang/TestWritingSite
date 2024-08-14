from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter(prefix="/writing")
templates = Jinja2Templates(directory="templates")


@router.get("/index", response_class=HTMLResponse)
def index(request: Request):
    pieces = [
        (path.name, True) if path.is_dir()
        else (path.stem, False)
        for path in Path("writing").iterdir()
    ]
    return templates.TemplateResponse(
        request=request,
        name="pages/writing_index.html",
        context={
            "pieces": pieces,
        }
    )


@router.get("/{piece}", response_class=HTMLResponse)
def piece(piece: str, request: Request):
    return templates.TemplateResponse(
        request=request,
        name="pages/story.html",
        context={
            "piece": piece,
            "content": Path(f"writing/{piece}.txt").read_text()
        },
    )


@router.get("/{piece}/{page}", response_class=HTMLResponse)
def story_page(piece: str, page: int, request: Request):
    next_page_exists = Path(f"writing/{piece}/{page + 1}.txt").exists()
    current_page_content = Path(f"writing/{piece}/{page}.txt").read_text()
    return templates.TemplateResponse(
        request=request,
        name="pages/story_page.html",
        context={
            "piece": piece,
            "current_page": page,
            "previous_page": page - 1 if page != 0 else None,
            "next_page": page + 1 if next_page_exists else None,
            "page_content": current_page_content,
        },
    )
