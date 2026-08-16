from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates
from fastapi import Request
import os

from .database import engine, Base
from . import models

from .routes.reviews import router as reviews_router
from .routes.requests import router as requests_router
from .routes.web_form import router as web_form_router
from .routes.dashboard import router as dashboard_router
from .routes.auth import router as auth_router


# ---------------------------------------------------------
# DATABASE
# ---------------------------------------------------------

Base.metadata.create_all(bind=engine)


# ---------------------------------------------------------
# APPLICATION
# ---------------------------------------------------------

app = FastAPI(
    title="AI-Powered Business Operations Automation System",
    description="AI-powered business request automation system",
    version="1.0.0"
)


# ---------------------------------------------------------
# SESSION MIDDLEWARE
# ---------------------------------------------------------

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY is not configured in the environment."
    )

app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    session_cookie="business_admin_session",
    max_age=60 * 60 * 8,
    same_site="lax",
    https_only=False
)


# ---------------------------------------------------------
# TEMPLATES
# ---------------------------------------------------------

templates = Jinja2Templates(
    directory="app/templates"
)


# ---------------------------------------------------------
# ROUTERS
# ---------------------------------------------------------

app.include_router(auth_router)
app.include_router(requests_router)
app.include_router(web_form_router)
app.include_router(dashboard_router)
app.include_router(reviews_router)


# ---------------------------------------------------------
# MAIN LANDING PAGE
# ---------------------------------------------------------

@app.get("/")
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="home.html"
    )