# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI

client = OpenAI(api_key="sk-4c53300b71df4f6a9b06a1096928b822", base_url="https://api.deepseek.com")
prompt = f"""
    Generate a comprehensive HTML presentation on: "cats"
    
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

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": prompt},
    ],
    stream=False
)

print(response.choices[0].message.content)