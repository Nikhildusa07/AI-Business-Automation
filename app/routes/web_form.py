from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import RequestCreate
from .requests import create_request


router = APIRouter(
    prefix="/web",
    tags=["Web Form"]
)

templates = Jinja2Templates(
    directory="app/templates"
)


@router.get("/", response_class=HTMLResponse)
def web_form(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="request_form.html"
    )


@router.post("/submit", response_class=HTMLResponse)
def submit_web_form(
    request: Request,
    customer_name: str = Form(...),
    customer_email: str = Form(...),
    input_text: str = Form(...),
    db: Session = Depends(get_db)
):

    request_data = RequestCreate(
        customer_name=customer_name,
        customer_email=customer_email,
        input_text=input_text
    )

    result = create_request(
        request_data=request_data,
        db=db
    )

    return templates.TemplateResponse(
        request=request,
        name="request_success.html",
        context={
            "result": result
        }
    )