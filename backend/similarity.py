from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load AI embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Job Description
job_description = """
Looking for AI Engineer with experience in Python,
FastAPI, React, SQL, Machine Learning, NLP,
and backend development.
"""

# Resume Text
resume_text = """
Python
React
SQL
FastAPI
Machine Learning

2 years experience in backend development and AI projects.
"""

# Convert text into embeddings
jd_embedding = model.encode(job_description)

resume_embedding = model.encode(resume_text)

# Calculate similarity
score = cosine_similarity(
    [jd_embedding],
    [resume_embedding]
)[0][0]

# Convert to percentage
match_percentage = round(score * 100, 2)

print("Resume Match Score:", match_percentage, "%")