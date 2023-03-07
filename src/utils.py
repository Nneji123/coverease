import openai
import os
from dotenv import load_dotenv

openai.api_key = os.getenv("OPENAI_KEY")

def generate_cover_letter(company_name, name, job_description, skills):
    prompt = f"""Write a cover letter addressed to {company_name} for the position of {job_description}. The cover letter should be addressed to {name}, and should highlight the following skills: {skills}."""
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.5,
        max_tokens=1024,
        n=1,
        stop=None,
        timeout=60,
    )
    cover_letter = response.choices[0].text.strip()
    return cover_letter

company_name = "Acme Inc."
name = "John Doe"
job_description = "Software Engineer"
skills = "Python, Django, React"

cover_letter = generate_cover_letter(company_name, name, job_description, skills)
print(cover_letter)