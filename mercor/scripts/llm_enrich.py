import os, json, openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def enrich_with_llm(applicant_json):
    prompt = f"""
    You are a recruiting analyst. Given this JSON applicant profile: {json.dumps(applicant_json)}
    Do four things:
    1. Provide a concise 75-word summary.
    2. Rate overall candidate quality from 1-10 (higher is better).
    3. List any data gaps or inconsistencies you notice.
    4. Suggest up to three follow-up questions to clarify gaps.

    Return exactly:
    Summary: <text>
    Score: <integer>
    Issues: <list or 'None'>
    Follow-Ups: <list>
    """

    resp = openai.completions.create(
        model="gpt-4",
        prompt=prompt,
        max_tokens=250,
        temperature=0
    )
    return resp.choices[0].text.strip()

if __name__ == "__main__":
    sample = {
        "personal": {"name": "Jane Doe", "location": "NYC"},
        "experience": [{"company": "Google", "title": "SWE"}],
        "salary": {"rate": 90, "currency": "USD", "availability": 25}
    }
    print(enrich_with_llm(sample))
