from openai import OpenAI

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)
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

    IMPORTANT: Return ONLY pure HTML without markdown or explanations.
    """


completion = client.chat.completions.create(
  extra_headers={
    "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
    "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
  },
  extra_body={},
  model="deepseek/deepseek-r1-0528:free",
  messages=[
    {
      "role": "user",
      "content": prompt
    }
  ]
)
print(completion.choices[0].message.content)