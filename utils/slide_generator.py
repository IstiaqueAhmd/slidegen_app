import os
import openai
from dotenv import load_dotenv
import json

from openai import OpenAI

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)

def generate_slides(topic, description):
    prompt = f"""
    Generate a comprehensive HTML presentation on: "{topic}"
    Description: {description}.
    
    Requirements:
    - Create the slides with DISTINCT Tailwind layouts (no two slides similar)
    - All slides must maintain 500px height and centered layout
    - Each slide must contain substantial content:
        * Title slide: Topic + meaningful subtitle
        * Content slides: 4-6 bullet points with detailed explanations
        * Visual slide: Detailed image description + 3 key insights
        * Conclusion: 4+ actionable takeaways
    - Layout diversity requirements:
        1. Title: Full-screen gradient with centered text
        2. Content Slide 1: Multi-column grid (2-3 columns) 
        3. Content Slide 2: Card-based layout with icons
        4. Content Slide 3: Split panel (text + visual elements)
        5. Visual Slide: Image focus with text overlay/caption
        6. Conclusion: Timeline/process flow OR numbered steps
        
    Design Guidelines:
    - Use varied background gradients (no repeat colors)
    - Mix text alignments (center/left/justified)
    - Incorporate different Heroicons for each content point
    - Apply diverse shadows/borders (rounded-xl, rounded-3xl, etc.)
    - Alternate between grid/flex layouts

    Return ONLY pure HTML without markdown or explanations.
    """

    try:
        completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
            "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
        },
        extra_body={},
        model="deepseek/deepseek-r1-distill-llama-70b:free",
        messages=[
            {
            "role": "user",
            "content": prompt
            }
        ])
        print(completion.choices[0].message.content)
        return completion.choices[0].message.content
    
    except Exception as e:
        print("OpenAI error:", e)
        return """
        <div class="w-full h-[500px] flex items-center justify-center bg-red-100 rounded-2xl shadow-lg">
          <div class="text-center p-8">
            <h2 class="text-3xl font-bold text-red-800 mb-4">Error</h2>
            <p class="text-xl text-red-600">Failed to generate slides. Please try again.</p>
          </div>
        </div>
        """