import os
import pdfplumber

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load AI model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Job Description
job_description = """
Looking for AI Engineer with experience in Python,
FastAPI, React, SQL, Machine Learning, NLP,
and backend development.
"""

# Convert JD into embedding
jd_embedding = model.encode(job_description)

resume_folder = "../resumes"

results = []

# Read all resumes
for filename in os.listdir(resume_folder):

    if filename.endswith(".pdf"):

        pdf_path = os.path.join(resume_folder, filename)

        text = ""

        with pdfplumber.open(pdf_path) as pdf:

            for page in pdf.pages:

                extracted = page.extract_text()

                if extracted:
                    text += extracted

        # Convert resume into embedding
        resume_embedding = model.encode(text)

        # Calculate similarity
        score = cosine_similarity(
            [jd_embedding],
            [resume_embedding]
        )[0][0]

        match_percentage = round(score * 100, 2)

        results.append((filename, match_percentage))

# Sort resumes by score
results.sort(key=lambda x: x[1], reverse=True)

print("\n===== Candidate Rankings =====\n")

for rank, result in enumerate(results, start=1):

    print(f"{rank}. {result[0]}")
    print(f"Match Score: {result[1]} %")
    print()