import os
import openai
from dotenv import load_dotenv
import json

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


'''def slides_perview(topic, description):
     
  prompt=f"""You are an expert presentation designer. Your task is to make a presentation on: {topic} and description: {description}.
  You have to return an array where each element is a slide. each element contains detailed explanation on what that particular slide should be like
  You will follow the given structure to generate the array with as many slides as needed to make the presentation better."""
  prompt +="""
  [
    {
        "title":,
        "content": ,
        "visuals":
    },
    {
        "title": ,
        "content": ,
        "visuals": 
    },
    {
        "title": ,
        "content": ,
        "visuals":
    },
    {
        "title": ,
        "content": ,
        "visuals":
    },
  ]
  IMPORTANT: Return only an array. No additional text or markup.
  """

  try:
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8
    )
    final_response = response.choices[0].message.content 
    print(type(final_response))
    print(final_response)
    return final_response

  except Exception as e:
    print("OpenAI error:", e)
    return """
    <div style="background: #ffebee; padding: 30px; border-radius: 16px; text-align: center;">
      <h2 style="color: #b71c1c;">Error</h2>
      <p>Failed to generate slides. Please try again.</p>
    </div>
    """'''
    


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
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.85  # Slightly higher for more creativity
        )
        return response.choices[0].message.content

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