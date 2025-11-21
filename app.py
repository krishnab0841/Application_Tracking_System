from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
import json
import traceback

load_dotenv() ## load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_gemini_repsonse(input):
    model = genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

# --- Prompts ---

prompt_score = """
Act as an expert ATS. Calculate the match score of the resume against the job description.
Provide a JSON response:
{{
  "score": "XX%",
  "breakdown": {{
    "skills_match": "XX%",
    "experience_match": "XX%",
    "education_match": "XX%"
  }},
  "reasoning": "Brief explanation of the score."
}}
resume: {text}
description: {jd}
"""

prompt_keywords = """
Act as an expert ATS. Identify matching and missing keywords.
Provide a JSON response:
{{
  "matching_keywords": ["key1", "key2"],
  "missing_keywords": ["key3", "key4"],
  "keyword_analysis": "Brief analysis of keyword usage."
}}
resume: {text}
description: {jd}
"""

prompt_rewrite = """
Act as an expert Resume Writer. Identify 3-5 weak bullet points in the resume and rewrite them to be more impactful and ATS-friendly (using action verbs, metrics).
Provide a JSON response:
{{
  "rewrites": [
    {{ "original": "original bullet", "improved": "improved bullet", "reason": "Why it is better" }}
  ]
}}
resume: {text}
description: {jd}
"""

prompt_summary = """
Act as an expert Resume Writer. Generate a professional summary for this candidate tailored to the job description.
Provide a JSON response:
{{
  "generated_summary": "The summary text..."
}}
resume: {text}
description: {jd}
"""

prompt_grammar = """
Act as an expert Editor. Identify grammar, spelling, and punctuation errors.
Provide a JSON response:
{{
  "errors": [
    {{ "error": "The error text", "correction": "The corrected text", "context": "Where it appears" }}
  ]
}}
resume: {text}
"""

prompt_format = """
Act as an expert ATS. Analyze the formatting and structure of the resume. Suggest improvements for better ATS parsing.
Provide a JSON response:
{{
  "suggestions": ["suggestion 1", "suggestion 2"]
}}
resume: {text}
"""

prompt_skills = """
Act as an expert ATS. Identify important skills missing from the resume based on the JD and suggest additions.
Provide a JSON response:
{{
  "missing_skills": ["skill 1", "skill 2"],
  "suggested_additions": ["suggestion 1", "suggestion 2"]
}}
resume: {text}
description: {jd}
"""

prompt_export = """
Act as an expert Resume Writer. Rewrite the entire resume content to be highly professional, ATS-friendly, and tailored to the job description. 
Keep the structure: Contact Info (placeholder), Summary, Skills, Experience, Education.
Return ONLY the plain text of the rewritten resume, no JSON, no markdown formatting.
resume: {text}
description: {jd}
"""

@app.post("/analyze")
async def analyze_resume(resume: UploadFile = File(...), jd: str = Form(...), action: str = Form(...)):
    try:
        if not resume.filename.endswith('.pdf'):
             raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        content = await resume.read()
        file_stream = io.BytesIO(content)
        text = input_pdf_text(file_stream)
        
        prompt_map = {
            "check_score": prompt_score,
            "keyword_match": prompt_keywords,
            "rewrite_bullets": prompt_rewrite,
            "summarize": prompt_summary,
            "grammar_check": prompt_grammar,
            "format_fix": prompt_format,
            "add_skills": prompt_skills
        }

        if action in prompt_map:
            prompt = prompt_map[action].format(text=text, jd=jd)
            response = get_gemini_repsonse(prompt)
            return {"response": response}
        
        elif action == "export_pdf":
            # Generate improved content
            prompt = prompt_export.format(text=text, jd=jd)
            improved_text = get_gemini_repsonse(prompt)
            
            # Create PDF
            buffer = io.BytesIO()
            c = canvas.Canvas(buffer, pagesize=letter)
            width, height = letter
            y = height - 50
            margin = 50
            
            c.setFont("Helvetica", 12)
            
            # Simple text wrapping
            lines = improved_text.split('\n')
            for line in lines:
                if y < 50:
                    c.showPage()
                    y = height - 50
                    c.setFont("Helvetica", 12)
                
                # Wrap long lines
                wrapped_lines = simpleSplit(line, "Helvetica", 12, width - 2*margin)
                for wrapped_line in wrapped_lines:
                    if y < 50:
                        c.showPage()
                        y = height - 50
                        c.setFont("Helvetica", 12)
                    c.drawString(margin, y, wrapped_line)
                    y -= 15
            
            c.save()
            buffer.seek(0)
            
            return StreamingResponse(
                buffer, 
                media_type="application/pdf", 
                headers={"Content-Disposition": "attachment; filename=improved_resume.pdf"}
            )

        else:
            raise HTTPException(status_code=400, detail="Invalid action")

    except Exception as e:
        traceback.print_exc()
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)