import os
from pymongo import MongoClient
from datetime import datetime
from fastapi import FastAPI, Request, Form, HTTPException, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse  
from fastapi.staticfiles import StaticFiles
from utils.slide_generator import generate_slides, generate_content, generate_reasoning
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed



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
async def generate(request: Request, topic: str = Form(...), description: str = Form(...)):
    slides = generate_content(topic, description)
    
    # Process slides in parallel
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Submit all tasks
        future_to_slide = {}
        for idx, slide in enumerate(slides):
            if slide:
                # Submit both tasks for the same slide
                future = executor.submit(
                    process_single_slide, 
                    slide, topic, description, idx
                )
                future_to_slide[future] = idx

        # Collect results as they complete
        all_slides_html = [None] * len(slides)
        all_reasonings = [None] * len(slides)
        
        for future in as_completed(future_to_slide):
            idx = future_to_slide[future]
            try:
                reasoning, html_slide = future.result()
                all_reasonings[idx] = reasoning
                all_slides_html[idx] = html_slide
            except Exception as e:
                print(f"Error processing slide {idx}: {e}")
                all_slides_html[idx] = error_slide_html(str(e))
    
    # Filter out None values
    all_reasonings = [r for r in all_reasonings if r is not None]
    all_slides_html = [s for s in all_slides_html if s is not None]
    
    # Save to MongoDB (same as before)
    uid = "4"
    slide_document = {
        "uid": uid,
        "topic": topic,
        "description": description,
        "reasonings": all_reasonings,
        "slides": all_slides_html,
        "created_at": datetime.utcnow(),
        "metadata": {
            "slide_count": len(all_slides_html),
            "app_version": "1.0"
        }
    }
    result = slides_collection.insert_one(slide_document)
    
    return templates.TemplateResponse(
        "slides.html", 
        {
            "request": request,
            "topic": topic,
            "slides_html": all_slides_html,
            "now": datetime.now().strftime("%Y-%m-%d")
        }
    )

def process_single_slide(slide, topic, description, idx):
    """Process both reasoning and HTML for a single slide"""
    reasoning = generate_reasoning(topic, slide, idx+1)
    html_slide = generate_slides(slide, topic, description)
    return reasoning, html_slide

def error_slide_html(error_msg):
    """Generate error slide HTML"""
    return f"""
    <div class="content-frame w-full max-w-4xl h-full flex items-center justify-center bg-red-100 rounded-xl shadow-lg p-8">
        <div class="text-center">
            <h2 class="text-3xl font-bold text-red-800 mb-4">Error</h2>
            <p class="text-xl text-red-600">{error_msg}</p>
        </div>
    </div>
    """

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="10.10.12.47", port=8000)