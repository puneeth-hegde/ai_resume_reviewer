import fitz  # PyMuPDF for PDFs
import docx

def extract_text(file):
    """Extract text from PDF or DOCX resume."""
    if file is None:
        return ""
    text = ""
    if file.name.endswith(".pdf"):
        pdf = fitz.open(stream=file.read(), filetype="pdf")
        for page in pdf:
            text += page.get_text()
    elif file.name.endswith(".docx"):
        document = docx.Document(file)
        for para in document.paragraphs:
            text += para.text + "\n"
    return text.strip()
