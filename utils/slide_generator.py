import os
import openai
from dotenv import load_dotenv
import json
import re
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv() 
DEEPSEEK_API_KEY=os.getenv("DEEPSEEK_API_KEY")

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key = DEEPSEEK_API_KEY,
)

def generate_content(user_input):
    prompt = f"""
    Create a presentation outline based on user input: "{user_input}"

    **Strict Requirements:**
    - Output ONLY a valid JSON array: ["Slide Title\\n• Bullet1\\n• Bullet2", ...]
    - Each slide format: "Title\\n• Concise bullet 1\\n• Concise bullet 2"
    - 3-5 bullets per slide (10-15 words each)
    - NEVER include: Slide numbers, markdown blocks, section headers, or explanations

    **Valid Example:**
    [
      "Renewable Energy\\n• Sustainable power sources\\n• Solar/wind/hydro solutions\\n• Reduced carbon footprint",
      "Solar Advantages\\n• Abundant resource\\n• Cost declining yearly\\n• Minimal maintenance required"
    ]

    **Output NOW:**
    """
    for attempt in range(3):  # Retry mechanism
        try:
            completion = client.chat.completions.create(
                model="deepseek/deepseek-r1-0528:free",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                top_p=0.9
            )
            raw = completion.choices[0].message.content.strip()
            return parse_slides(raw)
        except Exception:
            print(f"Attempt {attempt+1} failed, retrying...")
    return ["Generation Error\n• Please try different input"]  # Final fallback

def parse_slides(raw):
    """Robust JSON parsing with nested fallbacks"""
    # Clean common non-JSON artifacts
    cleaned = re.sub(r"```(json)?|^[^{[]*|[^}\]]*$", "", raw, flags=re.DOTALL)
    
    # Attempt 1: Direct JSON parsing
    try:
        slides = json.loads(cleaned)
        return [s.strip() for s in slides]
    except json.JSONDecodeError:
        pass
    
    # Attempt 2: Extract JSON substring
    try:
        json_str = re.search(r'\[([\s\S]*)\]', cleaned).group(0)
        slides = json.loads(json_str)
        return [s.strip() for s in slides]
    except (AttributeError, json.JSONDecodeError):
        pass
    
    # Attempt 3: Line-based parsing (fallback)
    slides = []
    current = []
    for line in re.split(r'\r?\n', cleaned):
        line = line.strip()
        if not line or line.startswith(("#", "Slide", "```")):
            continue  # Skip garbage
        
        if not line.startswith('•') and current:
            slides.append("\n".join(current))
            current = [line]  # New slide
        elif line.startswith('•') or not current:
            current.append(line)
    
    if current:
        slides.append("\n".join(current))
    
    return slides or ["Format Error\n• Received invalid response"]

def generate_reasoning(user_input, slide, num_of_slide):
    prompt = f"""
    You are currently generating the {num_of_slide}th slide based on the following user input:
    "{user_input}"
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
        print(f"Reasoning generation failed for {num_of_slide}th slide. Trying again...")
        generate_reasoning(user_input, slide, num_of_slide)

def generate_slides(slide, user_input):
    # Split slide into title and content
    parts = slide.split('\n', 1)
    slide_title = parts[0].strip()
    slide_content = parts[1].strip() if len(parts) > 1 else ""

    prompt = f"""
    Generate a presentation slide wrapped in a div tag.

    User Input: "{user_input}"

    Slide Content:
    Title: {slide_title}
    Body: {slide_content}

    Requirements:
    1. Return ONLY a div element containing the slide content
    2. The div must have these base classes: 
        "content-frame w-full max-w-4xl h-full p-8"
    3. Add appropriate Tailwind classes for:
        - Background gradients
        - Text alignment
        - Rounded corners (rounded-xl or rounded-3xl)
        - Shadows (shadow-lg or shadow-xl)
    4. Content must include:
        - Title as prominent heading (h1/h2)
        - Formatted body content
        - At least 1 relevant Heroicon
    5. Use one of these layout approaches:
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
            return generate_slides(slide, user_input)
    
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