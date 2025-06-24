import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_slides(topic, description):
    prompt = f"""
    Generate an HTML presentation on the topic: "{topic}".
    User description: "{description}"
    
    Requirements:
    - Create 5-7 slides with different layouts
    - Each slide should have a unique design (different colors, layouts, etc.)
    - Use inline CSS for styling each slide
    - Slides should include:
        * Title slide
        * Content slides with bullet points
        * Visual slides with relevant emojis
        * Conclusion slide
    
    Example slide formats:
    Slide 1: 
    <div style="background: linear-gradient(135deg, #4361ee, #3a0ca3); color: white; padding: 40px; border-radius: 16px; text-align: center;">
      <h1 style="font-size: 3rem;">{{TITLE}}</h1>
      <p style="font-size: 1.5rem; opacity: 0.9;">{{SUBTITLE}}</p>
    </div>
    
    Slide 2:
    <div style="background: #f8f9fa; border-left: 5px solid #4cc9f0; padding: 30px; border-radius: 16px;">
      <h2 style="color: #3a0ca3;">{{HEADING}}</h2>
      <ul style="list-style-type: circle; padding-left: 20px;">
        <li style="margin-bottom: 10px;">{{POINT}}</li>
      </ul>
    </div>
    
    Return only HTML code without any markdown or additional text.
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8
        )
        print(response.choices[0].message.content)
        return response.choices[0].message.content

    except Exception as e:
        print("OpenAI error:", e)
        return """
        <div style="background: #ffebee; padding: 30px; border-radius: 16px; text-align: center;">
          <h2 style="color: #b71c1c;">Error</h2>
          <p>Failed to generate slides. Please try again.</p>
        </div>
        """