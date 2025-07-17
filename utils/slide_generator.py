import os
import openai
from dotenv import load_dotenv
import json
import re
from openai import OpenAI
import httpx

# Modify client initialization
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
    http_client=httpx.Client(
        limits=httpx.Limits(
            max_connections=20,
            max_keepalive_connections=10
        ),
        timeout=httpx.Timeout(30.0)
    )
)


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


def generate_reasoning(topic, slide, num_of_slide):
    prompt = f"""
    You are currently generating the {num_of_slide}th slide on {topic}.
    Your current slide contents are: {slide}.
    You are given a task to generate a presentation slide wrapped in html(div) tag.
    Now, write your reasoning in brief on how you would generate this slide and how you would use the contents. 
    Return just your reasoning in as a string. 
    """
    try:
        completion = client.chat.completions.create(
            model="deepseek/deepseek-r1-0528:free",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3, 
            top_p=0.9
        )
        output = completion.choices[0].message.content.strip()
        return output
    except Exception as e:
        pass

def generate_slides(slide, topic, description):
    # Split slide into title and content
    parts = slide.split('\n', 1)
    slide_title = parts[0].strip()
    slide_content = parts[1].strip() if len(parts) > 1 else ""

    prompt = f"""
    Generate a presentation slide wrapped in a div tag.

    Presentation Topic: "{topic}"
    Presentation Description by user: "{description}"

    Slide Content:
    Title: {slide_title}
    Body: {slide_content}

    Requirements:
    1. Return ONLY a div element containing the slide content
    2. The div must have these base classes: 
        "content-frame w-full max-w-4xl h-full p-8"
    3. Use "className" instead of "class"
    4. Add appropriate Tailwind classes for:
        - Background gradients
        - Text alignment
        - Rounded corners (rounded-xl or rounded-3xl)
        - Shadows (shadow-lg or shadow-xl)
    5. Content must include:
        - Title as prominent heading (h1/h2)
        - Formatted body content
        - At least 1 relevant Heroicon
    6. Use one of these layout approaches:
        - Title Slide: Centered text with gradient
        - Content Slide: Multi-column grid (grid-cols-2/3)
        - Visual Slide: Split panel layout
        - Conclusion: Timeline/flow layout

    Return ONLY the div element without any additional HTML structure.
    """

    try:
        completion = client.chat.completions.create(
            model="deepseek/deepseek-r1-0528:free",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4, 
            top_p=0.9
        )
        output = completion.choices[0].message.content
        
        # Validate output is a div
        if output.strip().startswith('<div') and output.strip().endswith('</div>'):
            return output
        else:
            # Retry if output format is invalid
            return generate_slides(slide, topic, description)
    
    except Exception as e:
        print("OpenAI error:", e)
        return f"""
        <div class="content-frame w-full max-w-4xl h-full flex items-center justify-center bg-red-100 rounded-xl shadow-lg p-8">
            <div class="text-center">
                <h2 class="text-3xl font-bold text-red-800 mb-4">Error</h2>
                <p class="text-xl text-red-600">Failed to generate slide: {str(e)}</p>
            </div>
        </div>
        """