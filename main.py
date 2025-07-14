import os
from pymongo import MongoClient
from datetime import datetime
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse  
from fastapi.staticfiles import StaticFiles
from utils.slide_generator import generate_slides, generate_content
from bson import ObjectId

from dotenv import load_dotenv
load_dotenv()  

# Get MongoDB connection string from environment variable
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")

# Connect to MongoDB
client = MongoClient(MONGODB_URI)
db = client.get_database("slide_generator")  # Creates database if not exists
slides_collection = db.slides  # Creates collection if not exists

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate", response_class=HTMLResponse)
async def generate(request: Request, topic: str = Form(...), description: str = Form(...)):
    slides = generate_content(topic, description)
    all_slides = []
    for slide in slides:
        html_slide = generate_slides(slide, topic, description)
        print(html_slide)
        if html_slide:
            all_slides.append(html_slide)


    # Create document to save
    slide_document = {
        "topic": topic,
        "description": description,
        "slides": all_slides,
        "created_at": datetime.utcnow(),
        "metadata": {
            "slide_count": len(all_slides),
            "app_version": "1.0"
        }
    }

    # Insert into MongoDB
    result = slides_collection.insert_one(slide_document)
    print(f"Inserted document with ID: {result.inserted_id}")
    
    return templates.TemplateResponse(
        "slides.html", 
        {
            "request": request,
            "topic": topic,
            "slides_html": all_slides,
            "now": datetime.now().strftime("%Y-%m-%d")
        }
    )


@app.get("/slides/{slide_id}")
async def get_slides(slide_id: str):
    try:
        obj_id = ObjectId(slide_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid slide ID format")
    
    document = slides_collection.find_one({"_id": obj_id})
    
    if not document:
        raise HTTPException(status_code=404, detail="Slide set not found")
    
    return JSONResponse(content={"slides": document["slides"]})

@app.get("/slides", response_class=HTMLResponse)
async def list_slides(request: Request):
    # Get last 20 slide sets sorted by creation date
    slides_sets = slides_collection.find().sort("created_at", -1).limit(20)
    
    # Convert to list and format data
    slides_list = []
    for slide_set in slides_sets:
        slides_list.append({
            "id": str(slide_set["_id"]),
            "topic": slide_set["topic"],
            "created_at": slide_set["created_at"].strftime("%Y-%m-%d %H:%M"),
            "slide_count": len(slide_set["slides"])
        })
    
    return templates.TemplateResponse(
        "slide_list.html",
        {
            "request": request,
            "slides_list": slides_list
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.2", port=8000)