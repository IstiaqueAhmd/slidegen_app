import os
import openai
from dotenv import load_dotenv
import json

# Load environment variables from .env
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_slides(topic, description):
    prompt = f"""
    Generate presentation slides on the topic: "{topic}".
    The user has included this in the description: "{description}"
    Each slide should include:
    - A slide title
    3–5 bullet points (concise, not full sentences)

    Return the result in this exact JSON format:
    [
        {{
            "title": "Slide Title",
            "points": ["point1", "point2", "point3"]
        }},
        ...
    ]
    """

    try: 
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        content = response.choices[0].message.content
        slides = json.loads(content)
        return slides

    except Exception as e:
        print("OpenAI error:", e)
        return [{
            "title": "Error",
            "points": ["Failed to generate slides. Please try again."]
        }]