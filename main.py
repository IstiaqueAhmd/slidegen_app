from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,FileResponse
from fastapi.staticfiles import StaticFiles
from utils.slide_generator import generate_slides, generate_content

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

from datetime import datetime

@app.post("/generate", response_class=HTMLResponse)
async def generate(request: Request, topic: str = Form(...), description: str = Form(...)):    
    slides = generate_content(topic, description)
    all_slides = []
    for slide in slides:
        html_slide = generate_slides(slide,topic,description)
        all_slides.append(html_slide)
        print(html_slide)
    return templates.TemplateResponse(
        "slides.html", 
        {
            "request": request,
            "topic": topic,
            "slides_html": all_slides[0],
            "now": datetime.now().strftime("%Y-%m-%d")
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.2", port=8000)