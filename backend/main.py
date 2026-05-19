import os
import re
import pdfplumber

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize FastAPI
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load AI model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Upload folder
UPLOAD_FOLDER = "uploaded_resumes"

# Create folder if not exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Skills list
skills_list = [
    "Python",
    "FastAPI",
    "React",
    "SQL",
    "Machine Learning",
    "NLP",
    "JavaScript",
    "Docker",
    "MongoDB",
    "HTML",
    "CSS",
    "Flask",
    "Django",
    "Node.js",
    "Express",
    "Git",
    "REST API"
]

# Home Route
@app.get("/")
def home():

    return {
        "message": "AI Resume Screening API Running Successfully"
    }

# Resume Screening Route
@app.post("/analyze")
async def analyze_resume(

    job_description: str = Form(...),

    resume1: UploadFile = File(...),
    resume2: UploadFile = File(...),
    resume3: UploadFile = File(...),
    resume4: UploadFile = File(...)

):

    # Store resumes in list
    resumes = [resume1, resume2, resume3, resume4]

    results = []

    # Convert Job Description into embedding
    jd_embedding = model.encode(job_description)

    # Process each resume
    for resume in resumes:

        try:

            # Save uploaded file
            file_path = os.path.join(
                UPLOAD_FOLDER,
                resume.filename
            )

            with open(file_path, "wb") as f:

                f.write(await resume.read())

            # Extract text from PDF
            text = ""

            with pdfplumber.open(file_path) as pdf:

                for page in pdf.pages:

                    extracted = page.extract_text()

                    if extracted:
                        text += extracted

            # Check empty resume
            if text.strip() == "":

                results.append({
                    "resume": resume.filename,
                    "error": "No text found in resume"
                })

                continue

            # Convert resume into embedding
            resume_embedding = model.encode(text)

            # Similarity score
            score = cosine_similarity(
                [jd_embedding],
                [resume_embedding]
            )[0][0]

            # Convert to percentage
            match_percentage = round(score * 100, 2)

            # Skill Matching
            matched_skills = []

            for skill in skills_list:

                if skill.lower() in text.lower():

                    matched_skills.append(skill)

            # Candidate Status
            if match_percentage >= 70:

                status = "Selected"

            elif match_percentage >= 50:

                status = "Average Match"

            else:

                status = "Rejected"

            # Experience Detection
            if "experience" in text.lower():

                experience = "Experience Available"

            else:

                experience = "Fresher"

            # Email Extraction
            email_match = re.findall(
                r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
                text
            )

            email = (
                email_match[0]
                if email_match
                else "Email Not Found"
            )

            # Phone Number Extraction
            phone_match = re.findall(
                r"\+?\d[\d -]{8,12}\d",
                text
            )

            phone = (
                phone_match[0]
                if phone_match
                else "Phone Number Not Found"
            )

            # Shortlisted Reason
            shortlisted_reason = (
                "Strong match for required skills and job description"
            )

            # Store Results
            results.append({

                "resume": resume.filename,

                "match_score": match_percentage,

                "status": status,

                "matched_skills": matched_skills,

                "experience": experience,

                "email": email,

                "phone": phone,

                "shortlisted_reason": shortlisted_reason

            })

        except Exception as e:

            results.append({
                "resume": resume.filename,
                "error": str(e)
            })

    # Sort results by score
    results.sort(
        key=lambda x: x.get("match_score", 0),
        reverse=True
    )

    # Final Response
    return {
        "job_description": job_description,
        "total_resumes_screened": len(resumes),
        "rankings": results
    }