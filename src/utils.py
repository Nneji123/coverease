import openai
import os
from dotenv import load_dotenv
from models import Letter, db, User

load_dotenv()

openai.api_key = os.getenv("OPENAI_KEY")

def generate_cover_letter(company_name, name, job_description, skills):
    """
    The generate_cover_letter function takes in a company name, job description, and list of skills. It then uses the OpenAI API to generate a cover letter for the given inputs. The function returns the generated cover letter as a string.
    
    :param company_name: Address the company in the cover letter
    :param name: Personalize the cover letter
    :param job_description: Highlight the skills in the cover letter
    :param skills: Pass in the skills that you want to highlight in your cover letter
    :return: A string
    :doc-author: Trelent
    """
    prompt = f"""Write a cover letter addressed to {company_name} for the position of {job_description}. The cover letter should be addressed to hiring manager, and should highlight the following skills: {skills}. This is my name {name}.  The cover letter should be maximum 4 paragraphs long"""
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

def get_num_letters_for_user(user_id):
    num_letters = Letter.query.filter_by(user_id=user_id).count()
    return num_letters


def get_last_two_job_descriptions_for_user(user_id):
    letters = Letter.query.filter_by(user_id=user_id).order_by(Letter.id.desc()).limit(2).all()
    job_descriptions = [letter.job_description for letter in letters]
    return job_descriptions

def letter_history(user_id):
    letters = Letter.query.filter_by(user_id=user_id).all()
    return letters