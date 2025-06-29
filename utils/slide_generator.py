import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_slides(topic, description):
    prompt = f"""
    Generate an HTML presentation on: "{topic}".
    Description: "{description}"
    
    Requirements:
    - 5-7 slides with unique Tailwind layouts
    - The slides should contain detailed and useful information(up to date)
    - Only use Tailwind CSS classes
    - Each slide must be contained in a fixed-size container:
        * Width: 100% of parent container (max-w-5xl)
        * Height: 500px (h-[500px])
        * Centered with margins (mx-auto)
    - Slide types:
        1. Title slide (large centered text)
        2. Content slides (bullet points with icons)
        3. Image slides with placeholders
        4. Conclusion slide (call-to-action)
    
    Example formats:
    
    Slide 1:
    <div class="w-full h-[500px] flex flex-col items-center justify-center bg-gradient-to-r from-blue-600 to-indigo-900 p-8 rounded-2xl shadow-xl text-white mx-auto">
      <h1 class="text-5xl font-bold mb-4">Main Title</h1>
      <p class="text-2xl opacity-90">Subtitle Here</p>
    </div>
    
    Slide 2:
    <div class="w-full h-[500px] flex flex-col justify-center bg-gradient-to-br from-amber-100 to-orange-200 p-12 rounded-2xl shadow-xl mx-auto">
      <h2 class="text-4xl font-bold text-gray-800 mb-6">Section Heading</h2>
      <ul class="space-y-3 text-xl text-gray-700">
        <li class="flex items-start">
          <svg class="w-6 h-6 mr-2 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
          <span>Key point 1</span>
        </li>
      </ul>
    </div>
    
    Return ONLY pure HTML without markdown or explanations.
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
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