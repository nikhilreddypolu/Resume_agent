from google import genai
import os

def tailor_resume(base_resume_text, job_title, company, job_description, requirements):
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    
    reqs_str = "\n- ".join(requirements) if isinstance(requirements, list) else str(requirements)
    
    prompt = f"""
    You are an expert technical recruiter. Tailor this resume for the job.
    
    CONSTRAINTS:
    1. ZERO HALLUCINATION: Do not add any skills or experience not in the base resume.
    2. FORMATTING: Use plain text with clear headers and bullet points.
    3. NO CHATTER: Output ONLY the resume.

    TARGET JOB:
    Title: {job_title}
    Company: {company}
    Description: {job_description}
    Requirements: {reqs_str}
    
    BASE RESUME:
    {base_resume_text}
    
    TAILORED RESUME:
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=prompt
    )
    
    return response.text