from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter(prefix="/writing")
templates = Jinja2Templates(directory="templates")


@router.get("/index", response_class=HTMLResponse)
def index(request: Request):
    story_names = [
        path.name for path in Path("writing").iterdir() if path.is_dir()
    ]
    return templates.TemplateResponse(
        request=request,
        name="pages/writing_index.html",
        context={
            "story_names": story_names,
        }
    )


@router.get("/{story_name}/{page}", response_class=HTMLResponse)
def story_page(story_name: str, page: int, request: Request):
    next_page_exists = Path(f"writing/{story_name}/{page + 1}.txt").exists()
    current_page_content = Path(f"writing/{story_name}/{page}.txt").read_text()
    return templates.TemplateResponse(
        request=request,
        name="pages/story.html",
        context={
            "story_name": story_name,
            "current_page": page,
            "previous_page": page - 1 if page != 0 else None,
            "next_page": page + 1 if next_page_exists else None,
            "page_content": current_page_content,
        },
    )
