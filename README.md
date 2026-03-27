AI Resume Tailoring Agent
This is my submission for the Engineering Take-Home Challenge. I built an autonomous agent that takes a base resume and automatically rewrites it to match specific job descriptions using Gemini 2.5 Pro.

Why Option 2?
I chose the Resume Tailoring Agent because I wanted to build a pipeline that handles real-world data merging and strictly follows "Zero-Hallucination" rules—ensuring the AI only uses existing experience to match job requirements.

How it Works
Data Merging: Merges job data from option2_job_links.xlsx and option2_jobs.json using the ID field.

Extraction: Reads the base resume from Nikhil_Resume.docx.

Tailoring: A custom prompt instructs the LLM to act as a technical recruiter, highlighting relevant skills (like Python and Django) without inventing new ones.

Output: Saves a tailored .docx file for each job in the /outputs folder and logs a mock email delivery.

Setup & Running
1. Installation
Bash
# Clone and enter directory
git clone https://github.com/your-username/resume-agent
cd resume-agent

# Setup environment
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
2. Configuration
Create a .env file in the root directory:

Code snippet
GOOGLE_API_KEY=your_key_here
3. Execution
Bash
python main.py
Key Decisions
Gemini 2.5 Flash: Chosen for high speed and excellent instruction following.

Error Handling: The pipeline is fault-tolerant; if one job fails, the agent logs the error and continues to the next.

Integrity: Hard constraints in the prompt prevent the AI from adding fake skills.

Demo Video
[https://drive.google.com/file/d/1YUxG8rvJ65Vrsh_YWLGdnUfSCKohF91c/view?usp=sharing]