import os
from groq import Groq


client=Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_strategy(prompt):
    response=client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an expert cricket strategy analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content