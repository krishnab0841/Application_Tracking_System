from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from groq import Groq
import os
from dotenv import load_dotenv
import PyPDF2 as pdf
from docx import Document
from fpdf import FPDF
import io
import json
import re

load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Smart ATS API")

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper Functions
def extract_pdf_text(file_bytes):
    """Extract text from PDF bytes"""
    try:
        pdf_reader = pdf.PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error extracting PDF: {str(e)}")

def extract_docx_text(file_bytes):
    """Extract text from DOCX bytes"""
    try:
        doc = Document(io.BytesIO(file_bytes))
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\\n"
        return text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error extracting DOCX: {str(e)}")

def get_groq_response(prompt, max_tokens=2048):
    """Get response from Groq API"""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Groq API error: {str(e)}")

def parse_json_response(text):
    """Try to extract JSON from AI response"""
    try:
        return json.loads(text)
    except:
        json_match = re.search(r'\\{.*\\}', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except:
                pass
        return None

# Action Handlers
async def handle_check_score(resume_text, jd):
    """Handle ATS score checking with accurate analysis"""
    prompt = f"""You are an expert ATS analyzer. Analyze this resume against the job description and calculate a realistic ATS compatibility score.

Resume:
{resume_text}

Job Description:
{jd}

Calculate an ACCURATE overall match percentage (0-100%) based on how well the resume matches the JD. Analyze these categories:
- Skills Match: Compare required skills in JD vs resume
- Experience Match: Years and type of experience  
- Education Match: Educational requirements
- Keywords Match: Important terms from JD found in resume

Provide response in this EXACT JSON format:
{{"score": "XX%", "breakdown": {{"Skills Match": "XX%", "Experience Match": "XX%", "Education Match": "XX%", "Keywords Match": "XX%"}}, "reasoning": "Detailed explanation with specific strengths and gaps"}}

Return ONLY the JSON."""
    
    response = get_groq_response(prompt, max_tokens=1500)
    parsed = parse_json_response(response)
    return {"response": parsed} if parsed else {"response": {"score": "N/A", "breakdown": {}, "reasoning": response}}

async def handle_keyword_match(resume_text, jd):
    """Handle keyword matching analysis"""
    prompt = f"""Compare resume keywords with job description keywords.

Resume: {resume_text}

Job Description: {jd}

Provide response in this EXACT JSON format:
{{"matching_keywords": ["keyword1", "keyword2"], "missing_keywords": ["missing1", "missing2"], "keyword_analysis": "Brief analysis..."}}

Return ONLY the JSON."""
    
    response = get_groq_response(prompt)
    parsed = parse_json_response(response)
    return {"response": parsed} if parsed else {"response": {"matching_keywords": [], "missing_keywords": [], "keyword_analysis": response}}

async def handle_rewrite_bullets(resume_text, jd):
    """Handle bullet point rewriting"""
    prompt = f"""Improve bullet points from this resume to be more impactful and ATS-friendly.

Resume: {resume_text}

Job Description: {jd}

Provide response with at least 3 examples in EXACT JSON format:
{{"rewrites": [{{"original": "Original text", "improved": "Improved version", "reason": "Why it's better"}}]}}

Return ONLY the JSON."""
    
    response = get_groq_response(prompt, max_tokens=2500)
    parsed = parse_json_response(response)
    return {"response": parsed} if parsed else {"response": {"rewrites": [{"original": "Unable to parse", "improved": response, "reason": "Not in expected format"}]}}

async def handle_summarize(resume_text, jd):
    """Handle resume summarization"""
    prompt = f"""Create a professional summary for this resume based on the job description.

Resume: {resume_text}

Job Description: {jd}

Provide response in JSON format:
{{"professional_summary": "3-4 sentence summary...", "key_strengths": ["Strength 1", "Strength 2"]}}

Return ONLY the JSON."""
    
    response = get_groq_response(prompt)
    parsed = parse_json_response(response)
    return {"response": parsed} if parsed else {"response": {"professional_summary": response, "key_strengths": []}}

async def handle_grammar_check(resume_text, jd):
    """Handle grammar checking"""
    prompt = f"""Review this resume for grammar, spelling, and punctuation errors.

Resume: {resume_text}

Provide response in EXACT JSON format:
{{"errors": [{{"error": "Problematic text", "correction": "Corrected version", "context": "Context"}}]}}

If no errors: {{"errors": []}}

Return ONLY the JSON."""
    
    response = get_groq_response(prompt)
    parsed = parse_json_response(response)
    return {"response": parsed} if parsed else {"response": {"errors": []}}

async def handle_format_fix(resume_text, jd):
    """Handle format fixing suggestions"""
    prompt = f"""Analyze this resume and provide formatting improvement suggestions for ATS compatibility.

Resume: {resume_text}

Provide response in JSON format:
{{"formatting_suggestions": ["Tip 1", "Tip 2"], "section_order": ["Order"], "overall_feedback": "Assessment"}}

Return ONLY the JSON."""
    
    response = get_groq_response(prompt)
    parsed = parse_json_response(response)
    return {"response": parsed} if parsed else {"response": {"formatting_suggestions": [response], "section_order": [], "overall_feedback": "See above"}}

async def handle_add_skills(resume_text, jd):
    """Handle missing skills identification"""
    prompt = f"""Identify important skills missing from the resume based on the job description.

Resume: {resume_text}

Job Description: {jd}

Provide response in EXACT JSON format:
{{"technical_skills": ["Skill 1"], "soft_skills": ["Skill 1"], "certifications": ["Cert 1"], "tools_technologies": ["Tool 1"], "recommendations": "Where to add"}}

Return ONLY the JSON."""
    
    response = get_groq_response(prompt)
    parsed = parse_json_response(response)
    return {"response": parsed} if parsed else {"response": {"technical_skills": [], "soft_skills": [], "certifications": [], "tools_technologies": [], "recommendations": response}}

async def handle_export_pdf(resume_text, jd):
    """Handle PDF export of improved resume"""
    prompt = f"""Generate an improved, ATS-optimized version of this resume based on the job description.

Original Resume: {resume_text}

Job Description: {jd}

Create a complete improved resume with professional summary, optimized work experience, skills, and education. Format cleanly with clear section headings."""
    
    improved_content = get_groq_response(prompt, max_tokens=3000)
    
    pdf_file = FPDF()
    pdf_file.add_page()
    pdf_file.set_font("Arial", size=10)
    
    for line in improved_content.split('\\n'):
        line = line.encode('latin-1', 'replace').decode('latin-1')
        pdf_file.multi_cell(0, 5, txt=line, align='L')
    
    pdf_bytes = pdf_file.output(dest='S').encode('latin-1')
    
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=improved_resume.pdf"}
    )

# Main Endpoint
@app.post("/analyze")
async def analyze(resume: UploadFile = File(...), jd: str = Form(...), action: str = Form(...)):
    """Main endpoint for all ATS analysis actions"""
    
    file_bytes = await resume.read()
    
    if resume.filename.endswith('.pdf'):
        resume_text = extract_pdf_text(file_bytes)
    elif resume.filename.endswith('.docx'):
        resume_text = extract_docx_text(file_bytes)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file format. Please upload PDF or DOCX.")
    
    action_handlers = {
        "check_score": handle_check_score,
        "keyword_match": handle_keyword_match,
        "rewrite_bullets": handle_rewrite_bullets,
        "summarize": handle_summarize,
        "grammar_check": handle_grammar_check,
        "format_fix": handle_format_fix,
        "add_skills": handle_add_skills,
        "export_pdf": handle_export_pdf
    }
    
    handler = action_handlers.get(action)
    if not handler:
        raise HTTPException(status_code=400, detail=f"Invalid action: {action}")
    
    result = await handler(resume_text, jd)
    return result

# Health check endpoints
@app.get("/")
async def root():
    return {"message": "Smart ATS API is running", "status": "healthy"}

@app.get("/health")
async def health():
    return {"status": "healthy", "groq_configured": bool(os.getenv("GROQ_API_KEY"))}
