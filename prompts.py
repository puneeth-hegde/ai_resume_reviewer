def resume_review_prompt(resume_text, job_role):
    return f"""
    You are an ATS (Applicant Tracking System) and career advisor.
    Analyze this resume for a **{job_role}** role.

    Resume:
    {resume_text}

    Provide:
    1. ATS score (out of 100)
    2. Missing keywords/tools/skills for {job_role}
    3. 5 bullet-point actionable improvements
    4. A 2-line summary of your review
    """

def jd_match_prompt(resume_text, jd_text):
    return f"""
    Compare this resume with the job description and provide:
    1. JD match score (%) out of 100
    2. Key strengths
    3. Gaps that must be addressed
    Resume:
    {resume_text}

    Job Description:
    {jd_text}
    """
