
import os
from pymongo import MongoClient
from datetime import datetime
from fastapi import FastAPI, Request, Form, HTTPException, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse  
from fastapi.staticfiles import StaticFiles
from utils.slide_generator import generate_slides, generate_content, generate_reasoning
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Get MongoDB connection string from environment variable
load_dotenv() 
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")

# Connect to MongoDB
client = MongoClient(MONGODB_URI)
db = client.get_database("slide_generator")  # Creates database if not exists
slides_collection = db.slides  # Creates collection if not exists

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate", response_class=HTMLResponse)
async def generate(request: Request, user_input: str = Form(...)):
    slides = generate_content(user_input)
    all_slides = []
    all_reasonings = []
    for idx, slide in enumerate(slides):
        if slide:
            reasoning = generate_reasoning(user_input, slide, idx)
            html_slide = generate_slides(slide, user_input)
            print(reasoning)
            print(html_slide)
            if reasoning:
                all_reasonings.append(reasoning)
            if html_slide:
                all_slides.append(html_slide)
    
    #Hardcoding UID for now
    uid: str = "4"
    # Create document to save
    slide_document = {
        "uid": uid,
        "user_input": user_input,
        "reasonings": all_reasonings,
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
            "topic": user_input,
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

@app.get("/slides/user/{uid}")
async def get_user_slides(uid: str):
    try:
        user_docs = slides_collection.find({"uid": uid})

        all_slides = []
        for doc in user_docs:
            slides = doc.get("slides", [])
            all_slides.extend(slides)
            print()

        # Combine all slides into one string separated by marker
        response_string = "\n<!-- SLIDE BREAK -->\n".join(all_slides)
        return Response(content=response_string, media_type="text/plain")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving slides: {str(e)}")
    

@app.get("/slides/topic/{topic}")
async def get_user_slides(topic: str):
    try:
        user_docs = slides_collection.find({"topic": topic})

        all_slides = []
        for doc in user_docs:
            slides = doc.get("slides", [])
            all_slides.extend(slides)
            print()

        # Combine all slides into one string separated by marker
        response_string = "\n<!-- SLIDE BREAK -->\n".join(all_slides)
        return Response(content=response_string, media_type="text/plain")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving slides: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="10.10.12.47", port=8000)