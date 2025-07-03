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

    Return the output as a **Python list** (or **JSON array**), where each item contains the full content of one slide (with title and body).

    Format:
    [
      "Slide 1 Title\\nSlide 1 Body...",
      "Slide 2 Title\\nSlide 2 Body...",
      ...
    ]

    Do not write prose or explanation.
    """

    try:
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "<YOUR_SITE_URL>",
                "X-Title": "<YOUR_SITE_NAME>",
            },
            extra_body={},
            model="deepseek/deepseek-r1-0528:free",
            messages=[{"role": "user", "content": prompt}]
        )

        raw_output = completion.choices[0].message.content.strip()

        # Try to parse as JSON list first
        try:
            slides = json.loads(raw_output)
        except json.JSONDecodeError:
            # Fallback: try to extract slide content manually
            slides = re.split(r"\n?Slide \d+[:\-]?", raw_output)
            slides = [s.strip() for s in slides if s.strip()]

        print(f"[DEBUG] Total slides: {len(slides)}")
        for i, slide in enumerate(slides, 1):
            print(f"\n--- Slide {i} ---\n{slide}")

        return slides

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


def generate_slides(slide, topic, description):
    # Split slide into title and content
    parts = slide.split('\n', 1)
    slide_title = parts[0].strip()
    slide_content = parts[1].strip() if len(parts) > 1 else ""

    prompt = f"""
    Generate a complete HTML page for one presentation slide.

    Presentation Topic: "{topic}"
    Presentation Description: "{description}"

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
            extra_headers={
                "HTTP-Referer": "<YOUR_SITE_URL>",
                "X-Title": "<YOUR_SITE_NAME>",
            },
            model="deepseek/deepseek-r1-0528:free",
            messages=[{"role": "user", "content": prompt}]
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