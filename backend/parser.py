import os
import pdfplumber

resume_folder = "../resumes"

for filename in os.listdir(resume_folder):

    if filename.endswith(".pdf"):

        pdf_path = os.path.join(resume_folder, filename)

        text = ""

        with pdfplumber.open(pdf_path) as pdf:

            for page in pdf.pages:

                extracted = page.extract_text()

                if extracted:
                    text += extracted

        print("\n")
        print("=" * 50)
        print("Resume File:", filename)
        print("=" * 50)
        print(text)