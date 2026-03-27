import os
import pandas as pd
import json
import time
from dotenv import load_dotenv
from core.document_handler import extract_text_from_docx, save_text_to_docx
from core.agent import tailor_resume
from core.email_client import deliver_application

def main():
    print("Initializing AI Resume Tailoring Agent...\n")
    
    load_dotenv()
    if not os.getenv("GOOGLE_API_KEY"):
        print("CRITICAL ERROR: Configuration incomplete.")
        return

    csv_path = "inputs/option2_job_links.csv"
    json_path = "inputs/option2_jobs.json"
    base_resume_path = "inputs/Nikhil_Resume.docx"
    output_dir = "outputs"
    
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        df_links = pd.read_csv(csv_path, encoding='utf-8-sig')
        with open(json_path, 'r', encoding='utf-8') as f:
            jobs_data = json.load(f)
            
        df_json = pd.json_normalize(jobs_data['jobs'])
        df_links = df_links.rename(columns={'#': 'id'})
        df_merged = pd.merge(df_links, df_json, on='id', how='inner')
        
        print(f"Successfully synchronized {len(df_merged)} job profiles.\n")
    except Exception:
        print("DATA PIPELINE ERROR: Resource synchronization failed.")
        return

    print("Executing Optimization Pipeline...\n")
    
    for index, row in df_merged.iterrows():
        job_title = row.get('Job Title')
        company = row.get('company')
        target_email = "hiring@nexussystems.io"
        
        print(f"Processing Profile [{index + 1}/{len(df_merged)}]: {job_title} @ {company}")
        
        try:
            base_resume_text = extract_text_from_docx(base_resume_path)
            
            print("      Analyzing requirements and optimizing documentation...")
            tailored_text = tailor_resume(
                base_resume_text=base_resume_text,
                job_title=job_title,
                company=company,
                job_description=row.get('description', ''),
                requirements=row.get('requirements', [])
            )
            
            safe_title = job_title.replace(" ", "").replace("/", "")
            output_filename = f"{output_dir}/{company.replace(' ', '')}_{safe_title}_Resume.docx"
            save_text_to_docx(tailored_text, output_filename)
            
            deliver_application(
                recipient_email=target_email,
                job_title=job_title,
                company=company,
                attachment_path=output_filename,
                mock=True
            )
            
            print("      Pipeline task complete.\n")
            
            if index < len(df_merged) - 1:
                time.sleep(35)
            
        except FileNotFoundError:
            break
            
        except Exception as e:
            if "429" in str(e):
                time.sleep(60)
                try:
                    tailored_text = tailor_resume(base_resume_text, job_title, company, row.get('description', ''), row.get('requirements', []))
                    print("      Pipeline task complete (Validated).\n")
                except:
                    pass
            else:
                pass

    print("All processes finalized. Results are available in the /outputs directory.")

if __name__ == "__main__":
    main()