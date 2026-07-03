from pdf_generator import create_pdf
import streamlit as st
import PyPDF2
import google.generativeai as genai
from dotenv import load_dotenv
import os
from pypdf import PdfReader
import re

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text=""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Gemini Model
model = genai.GenerativeModel("gemini-2.5-flash")

# Streamlit Page
st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 CareerPilot AI")
st.subheader("Your Personal AI Career Mentor")

st.write("""
Welcome to CareerPilot AI!

### Features
- 📄 Resume Analyzer
- 🎯 ATS Score
- 📊 Skill Gap Analysis
- 🗺️ Career Roadmap
- 🎤 AI Interview Coach
- 📥 Download Career Report
""")
#-----
job_role = st.selectbox(
    "🎯 Select Your Target Job Role",
    ["Data Scientist", "Machine Learning Engineer", "Software Developer", "Data Analyst", "AI Engineer"]
)
#--------
# Resume Upload
uploaded_file = st.file_uploader(
    "📄 Upload Your Resume",
    type=["pdf"]
)

job_description = st.text_area(
    "📋 Paste Job Description",
    height=250
)

if uploaded_file is not None:

    st.success("✅ Resume uploaded successfully!")
    st.write("**File Name:**", uploaded_file.name)

    if st.button("🚀 Analyze Resume"):

        with st.spinner("📄 Reading Resume..."):

            pdf_reader = PyPDF2.PdfReader(uploaded_file)

            resume_text = ""

            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    resume_text += text

        if resume_text.strip():

            prompt = f"""
You are an expert ATS Resume Analyzer.

Analyze the following resume and provide:

1. ATS Score (out of 100)
2. Resume Summary:
(2-3 lines)
3. Strengths:
- Point 1
- Point 2
- Point 3
4. Weaknesses:
- Point 1
- Point 2
5. Missing Skills for {job_role}
- Skill 1
- Skill 2
6. Skill Gap Analysis:
7. Career Roadmap for {job_role}
- Step 1
- Step 2
- Step 3
8. Suggested Projects for {job_role}
- Project 1
- Project 2
9. Interview Questions for {job_role}
- Question 1
- Question 2
10. Final Suggestions:

11. Recommend the Top 3 Carrer Paths.

For each career provide:

- Career Name
- Match Score(%)
- Expected Salary(India)
- Required Skills
- Learning Roadmap

Resume:

{resume_text}
"""
            
        if job_description.strip():
            prompt += f"""
            Job Description:
            {job_description}

            Also provide:

            12. Resume Match Score(%)
            13. Matching Skills
            14. Missing Skills
            15. Resume Improvement Suggestions
            """

            with st.spinner("🤖 Gemini AI is analyzing your resume..."):
                response = model.generate_content(prompt)
                
                text_output = response.text

                match = re.search(r"ATS Score:\s*(\d+)",text_output)

                if match:
                    ats_score = int(match.group(1))
                else:
                    ats_score = 0
                    
            st.success("✅ Analysis Completed!")

            st.subheader("📊 AI Career Report")
            
            st.subheader("📄 Full AI Report")
            st.markdown(text_output)

            pdf_file = create_pdf(text_output)

            with open(pdf_file, "rb") as file:
                st.download_button(
                    label="📄 Download Career Report",
                    data=file,
                    file_name="Career_Report.pdf",
                    mime="application/pdf"
                    )
        else:
            st.error("❌ Could not extract text from the PDF.")

st.success("Ready to build your future? Upload your resume above!")