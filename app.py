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

# ==========================================
# AI INTERVIEW COACH
# ==========================================

st.divider()
st.header("🎤 AI Interview Coach")
st.write(
    "Practice a real interview with your AI career mentor. "
    "Answer each question and receive personalized feedback."
)

# Interview settings
interview_role = st.selectbox(
    "Select Interview Role",
    [
        "Data Scientist",
        "Data Analyst",
        "Machine Learning Engineer",
        "Software Developer",
        "AI Engineer"
    ],
    key="interview_role"
)

interview_type = st.selectbox(
    "Interview Type",
    [
        "Technical Interview",
        "HR Interview",
        "Project-Based Interview",
        "Mixed Interview"
    ],
    key="interview_type"
)

experience_level = st.selectbox(
    "Experience Level",
    ["Fresher", "Internship", "Experienced"],
    key="experience_level"
)

# Initialize interview session
if "interview_active" not in st.session_state:
    st.session_state.interview_active = False

if "interview_question" not in st.session_state:
    st.session_state.interview_question = ""

if "interview_history" not in st.session_state:
    st.session_state.interview_history = []

if "interview_count" not in st.session_state:
    st.session_state.interview_count = 0

if "interview_feedback" not in st.session_state:
    st.session_state.interview_feedback = ""

# Start interview
if st.button("🚀 Start Interview", key="start_interview"):

    try:
        with st.spinner("🤖 Interviewer is preparing your first question..."):

            prompt = f"""
You are a professional job interviewer.

Conduct a {interview_type} for a {experience_level}
candidate applying for the role of {interview_role}.

Ask exactly ONE relevant interview question.
Do not provide its answer.
Do not ask multiple questions at once.
Keep the question clear and professional.
"""

            response = model.generate_content(prompt)

            st.session_state.interview_question = response.text
            st.session_state.interview_history = []
            st.session_state.interview_count = 1
            st.session_state.interview_feedback = ""
            st.session_state.interview_active = True

    except Exception as e:
        st.error(f"Could not start interview: {e}")

# Display current question and answer form
if st.session_state.interview_active:

    st.subheader(
        f"Question {st.session_state.interview_count} of 5"
    )

    st.info(st.session_state.interview_question)

    answer = st.text_area(
        "✍️ Your Answer",
        key=f"interview_answer_{st.session_state.interview_count}",
        height=150,
        placeholder="Type your answer here..."
    )

    if st.button("📨 Submit Answer", key="submit_interview_answer"):

        if not answer.strip():
            st.warning("Please enter your answer first.")

        else:
            try:
                with st.spinner(
                    "🤖 Evaluating your answer and preparing the next question..."
                ):

                    evaluation_prompt = f"""
You are a professional interviewer and career coach.

Role: {st.session_state.interview_role}
Interview type: {st.session_state.interview_type}
Experience level: {st.session_state.experience_level}

Question:
{st.session_state.interview_question}

Candidate's answer:
{answer}

Evaluate the answer fairly.

Provide:
1. Score out of 10.
2. What the candidate did well.
3. What needs improvement.
4. A sample stronger answer.

Then decide whether another question is needed.
There are 5 questions in total.

If this was question 5, finish with:
INTERVIEW_COMPLETE

Otherwise, finish with:
NEXT_QUESTION:
followed by exactly one new interview question.
Do not provide the answer to the next question.
"""

                    result = model.generate_content(evaluation_prompt)
                    feedback = result.text or "No feedback was returned."

                    st.session_state.interview_history.append({
                        "question": st.session_state.interview_question,
                        "answer": answer,
                        "feedback": feedback
                    })

                    st.session_state.interview_feedback = feedback

                    if "INTERVIEW_COMPLETE" in feedback:
                        st.session_state.interview_active = False
                    else:
                        marker = "NEXT_QUESTION:"
                        if marker in feedback:
                            next_question = feedback.split(
                                marker, 1
                            )[1].strip()

                            st.session_state.interview_question = next_question
                            st.session_state.interview_count += 1
                        else:
                            st.session_state.interview_active = False
                            st.warning(
                                "The interviewer did not return the next "
                                "question in the expected format."
                            )

                st.rerun()

            except Exception as e:
                st.error(f"Interview error: {e}")

# Show the latest feedback
if st.session_state.interview_feedback:
    st.subheader("📊 Feedback on Your Answer")
    st.markdown(st.session_state.interview_feedback)

# Final interview summary
if (
    not st.session_state.interview_active
    and st.session_state.interview_history
    and st.session_state.interview_count >= 5
):
    st.success("🎉 Interview completed!")

    st.subheader("📋 Interview Summary")

    for index, item in enumerate(
        st.session_state.interview_history, start=1
    ):
        with st.expander(f"Question {index} — Review"):
            st.write("**Question:**", item["question"])
            st.write("**Your Answer:**", item["answer"])
            st.markdown(item["feedback"])

    if st.button("🔄 Start a New Interview"):
        st.session_state.interview_active = False
        st.session_state.interview_question = ""
        st.session_state.interview_history = []
        st.session_state.interview_count = 0
        st.session_state.interview_feedback = ""
        st.rerun()
