from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="Goal Governance",
    description="A web application for goal governance across decision, execution, and audit.",
    version="0.1.0",
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/", name="home")
async def home(request: Request):
    """Render the application home page."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"active_page": "home"},
    )


@app.get("/decision", name="decision")
async def decision(request: Request):
    """Render the decision module placeholder page."""
    return templates.TemplateResponse(
        request=request,
        name="decision.html",
        context={"active_page": "decision"},
    )


@app.get("/execution", name="execution")
async def execution(request: Request):
    """Render the execution module placeholder page."""
    return templates.TemplateResponse(
        request=request,
        name="execution.html",
        context={"active_page": "execution"},
    )


@app.get("/audit", name="audit")
async def audit(request: Request):
    """Render the audit module placeholder page."""
    return templates.TemplateResponse(
        request=request,
        name="audit.html",
        context={"active_page": "audit"},
    )
