import os
import openai
from dotenv import load_dotenv
import json
import re
from openai import OpenAI

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)

import re
import json

def generate_content(topic, description):
    prompt = f"""
    Generate a comprehensive presentation on: "{topic}"
    Description: {description}.

    **Output Requirements:**
    1. Return output STRICTLY as a JSON array: ["Title\\nBody", "Title\\nBody", ...]
    2. Each slide MUST follow format: "Title Text\\n• Bullet point 1\\n• Bullet point 2"
    3. NEVER include:
       - Slide numbers (e.g., "Slide 1:")
       - Markdown code blocks (```)
       - Section headers
       - Explanations outside slides
    4. Body content:
       - Use plain text with bullet points (•)
       - Maintain 3-5 bullet points per slide
       - Keep bullets concise (10-15 words each)

    Example of valid output:
    [
      "Renewable Energy\\n• Sustainable power sources\\n• Solar/wind/hydro solutions\\n• Reduced carbon footprint",
      "Solar Power Advantages\\n• Abundant resource\\n• Decreasing cost trend\\n• Low maintenance\\n• Scalable installations"
    ]
    """

    try:
        completion = client.chat.completions.create(
            model="deepseek/deepseek-r1-0528:free",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3, 
            top_p=0.9
        )

        raw_output = completion.choices[0].message.content.strip()
        parsed_slides = parse_slides(raw_output)
        print(parsed_slides)
        return parsed_slides
    except Exception as e:
        pass

def parse_slides(raw_output):
    """Robust parsing with JSON validation and fallback"""
    # Clean common artifacts
    cleaned = re.sub(r"```(json)?|^\[|\]$", "", raw_output, flags=re.MULTILINE).strip()
    
    # Attempt direct JSON parsing
    try:
        slides = json.loads(f"[{cleaned}]" if not cleaned.startswith('[') else cleaned)
        return [s.strip() for s in slides]
    except json.JSONDecodeError:
        pass
    
    # Fallback: Structural parsing
    slides = []
    current_slide = []
    
    for line in cleaned.split('\n'):
        if line.strip() and not re.match(r"^(Slide \d+|#+|[-*]{3,})", line):
            if not current_slide and line.strip():
                # New slide detected
                current_slide.append(line.strip())
            elif current_slide and line.startswith('•'):
                # Body content
                current_slide.append(line.strip())
            elif current_slide:
                # Slide complete
                slides.append("\n".join(current_slide))
                current_slide = [line.strip()]
    
    if current_slide:
        slides.append("\n".join(current_slide))
    
    return slides or [f"Format Error\n{raw_output}"]  # Fallback if parsing fails


def generate_slides(slide, topic, description):
    # Split slide into title and content
    parts = slide.split('\n', 1)
    slide_title = parts[0].strip()
    slide_content = parts[1].strip() if len(parts) > 1 else ""

    prompt = f"""
    Generate a complete HTML page for one presentation slide.

    Presentation Topic: "{topic}"
    Presentation Description by user: "{description}"

    Slide Content:
    Title: {slide_title}
    Body: {slide_content}

    Requirements:
    1. Return a COMPLETE HTML5 document including:
       - DOCTYPE declaration
       - Full HTML structure (<html>, <head>, <body>)
       - Head section with:
          * Title: {slide_title}
          * Tailwind CDN: <script src="https://cdn.tailwindcss.com"></script>
          * Heroicons CDN: <link href="https://cdn.jsdelivr.net/npm/heroicons@2.0.16/outline/icons.css" rel="stylesheet">

    2. Body structure (exact required structure):
        <body class="bg-gray-100">
          <div class="slide-container h-[500px] flex items-center justify-center p-8">
            <div class="content-frame w-full max-w-4xl h-full [slide-specific-styles]">
              <!-- YOUR SLIDE CONTENT HERE -->
            </div>
          </div>
        </body>

    3. Content Requirements:
       - Title must appear as prominent heading (h1/h2)
       - Body content must be formatted appropriately for slide type
       - Include at least 1 relevant Heroicon

    4. Design Guidelines:
       - Apply unique Tailwind utilities for each slide:
          * Background gradients
          * Text alignment variations
          * Rounded borders (rounded-xl/rounded-3xl)
          * Shadows (shadow-lg/shadow-xl)
       - Maintain 32px padding (p-8)
       - Fixed 500px height (h-[500px])
       - Max width 4xl (max-w-4xl)

    5. Layout Examples (apply ONE per slide):
       - Title Slide: Centered text with gradient background
       - Content Slide: Multi-column grid (grid-cols-2/3)
       - Visual Slide: Split panel (text + image description)
       - Conclusion: Timeline/flow layout

    Return ONLY pure HTML without markdown or explanations.
    """

    try:
        completion = client.chat.completions.create(
            model="deepseek/deepseek-r1-0528:free",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4, 
            top_p=0.9
        )
        return completion.choices[0].message.content
    
    except Exception as e:
        print("OpenAI error:", e)
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Error</title>
            <script src="https://cdn.tailwindcss.com"></script>
        </head>
        <body>
            <div class="w-full h-[500px] flex items-center justify-center bg-red-100">
                <div class="text-center p-8">
                    <h2 class="text-3xl font-bold text-red-800 mb-4">Error</h2>
                    <p class="text-xl text-red-600">Failed to generate slide: {str(e)}</p>
                </div>
            </div>
        </body>
        </html>
        """