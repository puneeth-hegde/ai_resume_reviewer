# AI Resume Reviewer (Streamlit + Gemini API)

An AI-powered **resume analysis tool** that reviews resumes against job roles and descriptions using **Google Gemini AI (1.5 Flash)**.  
It highlights missing skills, provides improvement tips, and generates **PDF reports**.

This project supports:
- Live Gemini API Mode (real AI analysis)  
- Demo Mode (mock results for offline/testing use)  

---

## Features
- Upload Resume (PDF/DOCX) → Extracts and processes text.
- Job Role Input → Tailors AI review for your target position.
- Optional JD Upload → Compares resume with job description.
- AI-Powered Review → Suggests missing skills & improvements.
- Highlighted Resume → Shows resume text with AI insights.
- PDF Report Generator → Downloadable review summary.
- Demo Mode Toggle → Works offline or without API key.

---

## Tech Stack
- Frontend: Streamlit (Python)
- AI Backend: Google Gemini 1.5 Flash (Generative AI API)
- PDF Parsing: PyPDF2 & python-docx
- PDF Report: FPDF
- Environment: Python 3.9+ (works on VS Code & Streamlit Cloud)

---

## Project Structure
```
ai_resume_reviewer/
│
├── app.py               # Streamlit UI + AI logic (demo/live toggle)
├── resume_parser.py      # PDF/DOCX text extraction
├── prompts.py            # Gemini prompt templates
├── utils.py              # PDF report generation & highlighting
├── requirements.txt      # Dependencies
└── README.md             # Documentation
```

---

## API Modes

### 1. Demo Mode (No API Key Needed)
- Instantly generates mock AI outputs for testing/demos.
- No internet or API calls required.
- Useful when Gemini API is slow or rate-limited.

### 2. Live Gemini API Mode (Real AI Analysis)
- Requires a valid GEMINI_API_KEY (Google AI Studio or paid Gemini API).
- Provides real AI-powered resume review.
- May experience timeouts or throttling on free-tier.

---

## Why Gemini API May Fail in Free Mode
- Free-tier has strict rate limits → Only a few requests/minute allowed.
- Large resume text slows responses (especially multi-chunk processing).
- API timeouts (504) occur if Google servers are overloaded.
- Our app uses timeouts + retries to prevent hanging, but falls back to Demo Mode if Gemini fails.

---

## Setup & Installation

### 1. Clone the Repo
```bash
git clone https://github.com/your-username/ai_resume_reviewer.git
cd ai_resume_reviewer
```

### 2. Create Virtual Environment & Install Dependencies
```bash
python -m venv .venv
source .venv/bin/activate    # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. (Optional) Configure Gemini API Key
- Sign up at https://makersuite.google.com/app/apikey
- Create an API key.
- Add to environment:
```bash
setx GEMINI_API_KEY "your_api_key_here"     # Windows (PowerShell)
export GEMINI_API_KEY="your_api_key_here"   # Mac/Linux
```

### 4. Run the App
```bash
streamlit run app.py
```

---

## Deployment
You can deploy on Streamlit Cloud:
1. Push code to GitHub.
2. Connect GitHub repo to https://share.streamlit.io.
3. Set GEMINI_API_KEY in app's secrets if using live API.

---

## Example Output
- Resume Review → Missing skills, ATS score, suggestions.
- JD Match Score → % match between resume and job description.
- PDF Report → Downloadable AI analysis.

## Sample Output Screenshots of Demo Mode (mock results for offline/testing use)  
![alt text](image.png)
![alt text](image-1.png)

---

## Key Learnings
- Integrated Gemini API for NLP tasks (resume analysis).
- Implemented fallback Demo Mode for offline/testing reliability.
- Learned about free API limitations (timeouts & throttling).
- Built Streamlit UI with real-time AI feedback.

---

## Future Improvements
- Deploy fully with paid Gemini API tier for faster, reliable analysis.
- Add keyword explainability for missing/matched skills.
- Support multi-resume batch analysis.
- Integrate ATS simulation scoring.

---

## License
This project is licensed under the MIT License.

---

## Contributors
- Puneeth Hegde – Resume parsing, AI pipeline, Streamlit UI, documentation.
