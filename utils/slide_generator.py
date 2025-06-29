import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_slides(topic, description):
    prompt = f"""
    Generate a comprehensive HTML presentation on: "{topic}".
    Description: "{description}"
    
    Requirements:
    - Create 6 slides with distinct Tailwind layouts (no two slides similar)
    - Each slide must contain substantial content (4-8 key points for content slides)
    - Slides must include:
        1. Title slide with topic and subtitle
        2. 3 content-rich slides with detailed information
        3. 1 visual slide with relevant image placeholder
        4. Conclusion slide with key takeaways
    - For content slides: Minimum 4 bullet points with 1-2 sentences each
    - Use diverse Tailwind utilities for unique designs:
        * Varied background gradients
        * Creative card layouts
        * Icon sets from Heroicons
        * Different text alignment patterns
        * Border and shadow variations
    
    Specific layout examples:
    
    Slide 1 (Title) - Centered with gradient:
    <div class="w-full h-[500px] flex flex-col items-center justify-center bg-gradient-to-br from-purple-900 via-blue-800 to-indigo-900 p-8 rounded-2xl shadow-2xl text-white mx-auto">
      <h1 class="text-5xl font-bold mb-4 text-center">{{TOPIC}}</h1>
      <p class="text-2xl opacity-90 text-center max-w-2xl">{{SUBTITLE}}</p>
    </div>
    
    Slide 2 (Content) - Split columns with icons:
    <div class="w-full h-[500px] flex items-center justify-center bg-gradient-to-tr from-amber-50 to-orange-100 p-12 rounded-2xl shadow-xl mx-auto">
      <div class="grid grid-cols-2 gap-10 max-w-6xl">
        <div>
          <h2 class="text-4xl font-bold text-gray-800 mb-6">Section 1</h2>
          <ul class="space-y-4 text-lg text-gray-700">
            <li class="flex items-start">
              <svg class="w-6 h-6 mr-3 text-green-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
              <span>Detailed point 1 with sufficient explanation to fill space properly</span>
            </li>
            <li class="flex items-start">
              <svg class="w-6 h-6 mr-3 text-green-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
              <span>Comprehensive point 2 with enough content to make slide substantial</span>
            </li>
          </ul>
        </div>
        <div>
          <h2 class="text-4xl font-bold text-gray-800 mb-6">Section 2</h2>
          <ul class="space-y-4 text-lg text-gray-700">
            <li class="flex items-start">
              <svg class="w-6 h-6 mr-3 text-blue-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
              <span>Additional detailed information with proper context and explanation</span>
            </li>
            <li class="flex items-start">
              <svg class="w-6 h-6 mr-3 text-blue-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
              <span>In-depth analysis point with supporting details</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
    
    Slide 3 (Visual) - Card layout with image:
    <div class="w-full h-[500px] flex items-center justify-center bg-gradient-to-r from-emerald-50 to-teal-100 p-8 rounded-2xl shadow-xl mx-auto">
      <div class="max-w-5xl grid grid-cols-2 gap-12 items-center">
        <div>
          <h2 class="text-4xl font-bold text-gray-800 mb-6">Visual Exploration</h2>
          <p class="text-lg text-gray-700 mb-6">Detailed explanation of the visual content and its relevance to the topic with sufficient context.</p>
          <ul class="space-y-3 text-lg text-gray-700">
            <li class="flex items-start">
              <svg class="w-5 h-5 mr-2 text-teal-600 mt-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>
              <span>Key insight derived from visual</span>
            </li>
            <li class="flex items-start">
              <svg class="w-5 h-5 mr-2 text-teal-600 mt-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>
              <span>Additional observation with explanation</span>
            </li>
          </ul>
        </div>
        <div class="bg-white/70 backdrop-blur-sm rounded-xl p-6 border border-gray-200 shadow-md">
          <img src="https://via.placeholder.com/600x400?text=Relevant+Visual" alt="Content visual" class="rounded-lg w-full">
          <p class="text-center text-gray-600 mt-3">Detailed caption explaining the visual</p>
        </div>
      </div>
    </div>
    
    Return ONLY pure HTML without markdown or explanations.
    Ensure each slide has substantial content and unique layout.
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