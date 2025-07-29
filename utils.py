import io
from fpdf import FPDF
import re

def generate_pdf_report(review_text: str, job_role: str, jd_match_text: str = "") -> bytes:
    """
    Generate a PDF report with resume analysis and optional JD match score.
    Returns PDF file in bytes format.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=14)

    pdf.cell(200, 10, txt="AI Resume Review Report", ln=True, align="C")
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=f"Target Job Role: {job_role}\n\n")

    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt="Resume Review:")
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 8, txt=review_text)

    if jd_match_text:
        pdf.ln(5)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt="Job Description Match Analysis:")
        pdf.set_font("Arial", size=11)
        pdf.multi_cell(0, 8, txt=jd_match_text)

    # Save PDF to bytes
    pdf_output = io.BytesIO()
    pdf_bytes = pdf.output(dest="S").encode("latin1")
    pdf_output.write(pdf_bytes)
    return pdf_output.getvalue()


def highlight_missing_keywords(resume_text: str, review_text: str) -> str:
    """
    Highlight missing keywords in the resume text (keywords identified in the review_text).
    """
    missing_keywords = re.findall(r"(?i)(?<=Missing Keywords:)(.*?)(?=Improvements|$)", review_text, re.S)
    if not missing_keywords:
        return resume_text  # No keywords found

    keywords = [k.strip() for k in missing_keywords[0].split("\n") if k.strip()]
    highlighted = resume_text
    for kw in keywords:
        if kw:
            highlighted = re.sub(
                fr"\b{re.escape(kw)}\b",
                f"<span style='color:red; font-weight:bold'>{kw}</span>",
                highlighted,
                flags=re.IGNORECASE,
            )
    return highlighted
