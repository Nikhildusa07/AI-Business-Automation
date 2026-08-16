import os

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


templates = Jinja2Templates(
    directory="app/templates"
)


# ---------------------------------------------------------
# LOGIN PAGE
# ---------------------------------------------------------

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )


# ---------------------------------------------------------
# LOGIN
# ---------------------------------------------------------

@router.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):

    admin_username = os.getenv("ADMIN_USERNAME")
    admin_password = os.getenv("ADMIN_PASSWORD")

    if not admin_username or not admin_password:

        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={
                "error": "Admin credentials are not configured."
            },
            status_code=500
        )

    if username == admin_username and password == admin_password:

        request.session.clear()

        request.session["admin_logged_in"] = True
        request.session["admin_username"] = username

        return RedirectResponse(
            url="/dashboard/",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "error": "Invalid username or password."
        },
        status_code=401
    )


# ---------------------------------------------------------
# LOGOUT
# ---------------------------------------------------------

@router.get("/logout")
def logout(request: Request):

    request.session.clear()

    return RedirectResponse(
        url="/",
        status_code=303
    )