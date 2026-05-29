import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def analyze_code(code, mode, language):

    if mode == "Explain":

        prompt = f"""
Return ONLY valid JSON.

Format:
{{
    "summary": "",
    "explanations": [],
    "warnings": [],
    "bugs": [],
    "fixes": []
}}

Explain this {language} code line by line.

Code:
{code}
"""

    elif mode == "Debug":

        prompt = f"""
Return ONLY valid JSON.

Format:
{{
    "summary": "",
    "explanations": [],
    "warnings": [],
    "bugs": [],
    "fixes": []
}}

Debug this {language} code.

Code:
{code}
"""

    else:

        prompt = f"""
Return ONLY valid JSON.

Format:
{{
    "summary": "",
    "explanations": [],
    "warnings": [],
    "bugs": [],
    "fixes": []
}}

Explain and debug this {language} code.

Code:
{code}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=2000
    )

    result = response.choices[0].message.content.strip()

# Remove markdown JSON wrappers
    result = result.replace("```json", "")
    result = result.replace("```", "")
    result = result.strip()

    try:
        data = json.loads(result)
        return data

    except:
        return {
            "summary": "Failed to parse AI response.",
            "explanations": [],
            "warnings": [],
            "bugs": [],
            "fixes": []
        }