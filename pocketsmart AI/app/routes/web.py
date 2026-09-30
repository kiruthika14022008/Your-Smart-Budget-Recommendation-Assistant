from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

router = APIRouter()


@router.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
        },
    )


@router.get("/home")
def home_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={
            "request": request,
        },
    )


@router.get("/planner/home")
def planner_home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={
            "request": request,
        },
    )


@router.get("/planner/party")
def planner_party(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="party.html",
        context={
            "request": request,
        },
    )


@router.get("/planner/jewelry")
def planner_jewelry(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="jewelry.html",
        context={
            "request": request,
        },
    )


@router.get("/dashboard")
def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "request": request,
        },
    )


@router.get("/jewelry")
def jewelry(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="jewelry.html",
        context={
            "request": request,
        },
    )


@router.get("/party")
def party(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="party.html",
        context={
            "request": request,
        },
    )


@router.get("/login")
def login(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "request": request,
        },
    )


@router.get("/register")
def register(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={
            "request": request,
        },
    )