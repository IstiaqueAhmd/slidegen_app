from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from utils.slide_generator import generate_slides

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate", response_class=HTMLResponse)
async def generate(request: Request, topic: str = Form(...), description: str = Form(...)):
    slides_html = generate_slides(topic, description)
    return templates.TemplateResponse(
        "slides.html", 
        {
            "request": request,
            "topic": topic,
            "slides_html": slides_html
        }
    )