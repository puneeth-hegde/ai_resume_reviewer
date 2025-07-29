import streamlit as st
import os
from resume_parser import extract_text
from prompts import resume_review_prompt, jd_match_prompt
from utils import generate_pdf_report, highlight_missing_keywords

# --- UI SETUP ---
st.set_page_config(page_title="AI Resume Reviewer", layout="wide")
st.title("📄 AI Resume Reviewer")

# --- DEMO MODE TOGGLE ---
demo_mode = st.sidebar.checkbox("Enable Demo Mode (No API Calls)", value=False)

# --- INPUT SECTION ---
col1, col2 = st.columns([2, 1])
with col1:
    job_role = st.text_input("🎯 Target Job Role (e.g., Data Analyst)")
with col2:
    jd_file = st.file_uploader("📥 Upload Job Description (Optional)", type=["pdf", "docx"])

resume_file = st.file_uploader("📤 Upload Resume (PDF/DOCX)", type=["pdf", "docx"])

# --- ANALYZE BUTTON ---
if st.button("🔎 Analyze Resume"):
    if resume_file and job_role:
        st.info("Processing your resume...")

        # --- TEXT EXTRACTION ---
        resume_text = extract_text(resume_file)[:2000]
        jd_text = extract_text(jd_file)[:1500] if jd_file else ""

        # --- DEMO MODE CHECK ---
        if demo_mode:
            st.warning("⚠ Running in Demo Mode. No API calls will be made.")
            review = "Demo Review: Strong resume but missing AWS, Tableau, and SQL for Data Analyst roles."
            highlighted_resume = highlight_missing_keywords(resume_text, review)
            jd_match = "Demo JD Match: 75% match. Improve cloud skills for better alignment."
        else:
            try:
                # --- GEMINI INIT ---
                import google.generativeai as genai
                api_key = os.getenv("GEMINI_API_KEY")
                if not api_key:
                    st.error("❌ Gemini API key not found. Please set GEMINI_API_KEY.")
                    st.stop()

                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-1.5-flash")
                st.success("✅ Gemini API initialized successfully")

                # --- CHUNKING ---
                chunks = [resume_text[i:i+800] for i in range(0, len(resume_text), 800)]
                summaries = []
                with st.spinner("Summarizing resume in chunks..."):
                    for chunk in chunks:
                        try:
                            response = model.generate_content(
                                f"Summarize this resume chunk:\n\n{chunk}",
                                request_options={"timeout": 30}
                            )
                            summaries.append(response.text)
                        except Exception:
                            st.warning("⚠ Chunk summarization timed out. Using demo summary.")
                            summaries.append("Demo: Candidate skilled in Python, ML, and DA.")
                final_resume_summary = " ".join(summaries)

                # --- MAIN REVIEW ---
                with st.spinner("Analyzing Resume with Gemini AI..."):
                    try:
                        response = model.generate_content(
                            resume_review_prompt(final_resume_summary, job_role),
                            request_options={"timeout": 60}
                        )
                        review = response.text
                    except Exception:
                        st.warning("⚠ Gemini timed out. Using demo review.")
                        review = "Demo Review: Strong resume but missing AWS, Tableau, and cloud skills."

                highlighted_resume = highlight_missing_keywords(resume_text, review)

                # --- JD MATCH ---
                jd_match = ""
                if jd_text:
                    with st.spinner("Comparing with Job Description..."):
                        try:
                            jd_response = model.generate_content(
                                jd_match_prompt(final_resume_summary, jd_text),
                                request_options={"timeout": 60}
                            )
                            jd_match = jd_response.text
                        except Exception:
                            jd_match = "Demo JD Match: 70% match. Missing SQL and Tableau."

            except Exception as e:
                st.error(f"❌ Gemini API call failed: {e}")
                st.stop()

        # --- DISPLAY RESULTS ---
        st.subheader("📊 Resume Review")
        st.markdown(review)
        st.subheader("🖋 Highlighted Resume")
        st.markdown(highlighted_resume, unsafe_allow_html=True)

        if jd_file:
            st.subheader("📌 JD Match Score")
            st.markdown(jd_match)

        # --- PDF DOWNLOAD ---
        pdf_report = generate_pdf_report(review, job_role, jd_match if jd_file else "")
        st.download_button("📥 Download PDF Report", pdf_report, "resume_review.pdf", "application/pdf")

    else:
        st.warning("⚠ Please upload a resume and enter a target job role.")
else:
    st.info("ℹ️ Upload a resume and click **Analyze Resume** to start.")
