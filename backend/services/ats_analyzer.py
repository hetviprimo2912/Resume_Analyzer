import json
import re

from pathlib import Path

from vectorstore.faiss_store import FAISSStore
from llm.model import generate_response


# ---------------------------------------------------------
# Common resume / technical skills
# ---------------------------------------------------------

KNOWN_SKILLS = {
    "python",
    "java",
    "javascript",
    "typescript",
    "c",
    "c++",
    "c#",
    ".net",
    "react",
    "react.js",
    "next.js",
    "nextjs",
    "node.js",
    "nodejs",
    "express",
    "express.js",
    "django",
    "flask",
    "fastapi",
    "spring",
    "spring boot",
    "html",
    "html5",
    "css",
    "tailwind",
    "tailwind css",
    "bootstrap",
    "redux",
    "redux toolkit",
    "angular",
    "vue",
    "vue.js",
    "mongodb",
    "mysql",
    "postgresql",
    "postgres",
    "sqlite",
    "sql",
    "firebase",
    "redis",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
    "git",
    "github",
    "gitlab",
    "jenkins",
    "ci/cd",
    "rest",
    "rest api",
    "graphql",
    "api",
    "machine learning",
    "deep learning",
    "tensorflow",
    "pytorch",
    "pandas",
    "numpy",
    "scikit-learn",
    "opencv",
    "data structures",
    "algorithms",
    "dbms",
    "oop",
    "jira",
    "postman",
    "figma",
    "linux",
    "bash",
    "php",
    "laravel",
    "ruby",
    "rails",
    "go",
    "golang",
    "rust",
    "kotlin",
    "swift",
}


# ---------------------------------------------------------
# Load complete resume from FAISS metadata
# ---------------------------------------------------------

def get_resume_text(resume_id: str) -> str:

    store_path = Path("storage") / resume_id

    if not store_path.exists():
        raise FileNotFoundError(
            f"Resume '{resume_id}' not found."
        )

    store = FAISSStore.load(
        str(store_path)
    )

    chunks = store.metadata

    # Preserve original chunk order.
    chunks = sorted(
        chunks,
        key=lambda x: (
            x.page,
            x.chunk_id
        )
    )

    parts = []

    for chunk in chunks:

        content = chunk.content.strip()

        if content:
            parts.append(content)

    return "\n".join(parts)


# ---------------------------------------------------------
# Normalize text
# ---------------------------------------------------------

def normalize_text(text: str) -> str:

    text = text.lower()

    text = text.replace("react.js", "react")
    text = text.replace("node.js", "nodejs")
    text = text.replace("next.js", "nextjs")
    text = text.replace("express.js", "express")

    return text


# ---------------------------------------------------------
# Extract known skills
# ---------------------------------------------------------

def extract_skills(text: str) -> list[str]:

    normalized = normalize_text(text)

    found = []

    # Longer phrases first so that
    # "machine learning" is checked before "learning".
    skills = sorted(
        KNOWN_SKILLS,
        key=len,
        reverse=True
    )

    for skill in skills:

        normalized_skill = normalize_text(skill)

        pattern = r"(?<![a-z0-9])" + re.escape(
            normalized_skill
        ) + r"(?![a-z0-9])"

        if re.search(pattern, normalized):

            # Normalize display names.
            display_skill = skill

            if display_skill not in found:
                found.append(display_skill)

    return found


# ---------------------------------------------------------
# Generate ATS score
# ---------------------------------------------------------

def calculate_ats_score(
    resume_text: str,
    job_description: str
):

    resume_skills = extract_skills(
        resume_text
    )

    jd_skills = extract_skills(
        job_description
    )
    print("\n========== ATS DEBUG ==========")
    print("Resume Skills:")
    print(resume_skills)

    print("\nJD Skills:")
    print(jd_skills)
    print("================================\n")
    resume_normalized = normalize_text(
        resume_text
    )

    jd_normalized = normalize_text(
        job_description
    )

    matched_skills = []
    missing_skills = []

    for skill in jd_skills:

        normalized_skill = normalize_text(
            skill
        )

        pattern = r"(?<![a-z0-9])" + re.escape(
            normalized_skill
        ) + r"(?![a-z0-9])"

        if re.search(
            pattern,
            resume_normalized
        ):
            matched_skills.append(skill)

        else:
            missing_skills.append(skill)

    # -----------------------------------------------------
    # Skill match percentage
    # -----------------------------------------------------

    if jd_skills:

        match_percentage = round(
            len(matched_skills)
            / len(jd_skills)
            * 100
        )

    else:

        match_percentage = 0

    # -----------------------------------------------------
    # Keyword relevance
    # -----------------------------------------------------

    jd_words = set(
        re.findall(
            r"\b[a-zA-Z][a-zA-Z0-9+#.-]{2,}\b",
            jd_normalized
        )
    )

    resume_words = set(
        re.findall(
            r"\b[a-zA-Z][a-zA-Z0-9+#.-]{2,}\b",
            resume_normalized
        )
    )

    stop_words = {
        "the",
        "and",
        "for",
        "with",
        "that",
        "this",
        "are",
        "you",
        "your",
        "our",
        "will",
        "have",
        "has",
        "from",
        "into",
        "about",
        "their",
        "they",
        "them",
        "job",
        "role",
        "work",
        "working",
        "candidate",
        "experience",
        "years",
        "year",
        "using",
        "used",
        "looking",
        "required",
        "requirements",
    }

    meaningful_jd_words = {
        word
        for word in jd_words
        if word not in stop_words
    }

    matched_keywords = (
        meaningful_jd_words
        & resume_words
    )

    if meaningful_jd_words:

        keyword_score = round(
            len(matched_keywords)
            / len(meaningful_jd_words)
            * 100
        )

    else:

        keyword_score = 0

    # -----------------------------------------------------
    # ATS score
    #
    # 60% skill relevance
    # 40% keyword relevance
    # -----------------------------------------------------

    ats_score = round(
        (match_percentage * 0.60)
        + (keyword_score * 0.40)
    )

    ats_score = max(
        0,
        min(
            100,
            ats_score
        )
    )

    return {
        "ats_score": ats_score,
        "match_percentage": match_percentage,
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "keyword_score": keyword_score,
    }


# ---------------------------------------------------------
# Generate feedback using existing Ollama model
# ---------------------------------------------------------

def generate_ats_feedback(
    resume_text: str,
    job_description: str,
    analysis: dict
):

    prompt = f"""
You are an ATS resume improvement assistant.

Use ONLY the resume and job description below.

Do not invent experience, skills, certifications,
projects, achievements, or technologies.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

ATS SCORE:
{analysis["ats_score"]}

MATCH PERCENTAGE:
{analysis["match_percentage"]}

MATCHED SKILLS:
{", ".join(analysis["matched_skills"])}

MISSING SKILLS:
{", ".join(analysis["missing_skills"])}

Return ONLY valid JSON using exactly this structure:

{{
    "strengths": [
        "short strength",
        "short strength",
        "short strength"
    ],
    "areas_to_improve": [
        "short improvement",
        "short improvement",
        "short improvement"
    ],
    "suggestions": [
        "short actionable suggestion",
        "short actionable suggestion",
        "short actionable suggestion"
    ]
}}

Rules:

Rules:

- Maximum 3 items in each array.
- Keep every item concise.
- Suggestions must be based on the resume and job description.
- Do not recommend claiming experience the candidate does not have.
- NEVER list a missing skill as a strength.
- Strengths MUST contain only skills or experience explicitly present in the resume.
- Areas to improve SHOULD focus on missing job requirements or weak resume presentation.
- Suggestions must be actionable and must not falsely imply that the candidate already has a missing skill.
"""

    try:

        response = generate_response(
            prompt
        )

        # Remove accidental markdown fences.
        response = response.strip()

        if response.startswith("```"):

            response = re.sub(
                r"^```(?:json)?",
                "",
                response,
                flags=re.IGNORECASE
            )

            response = re.sub(
                r"```$",
                "",
                response
            )

        data = json.loads(
            response.strip()
        )

        return {
            "strengths": data.get(
                "strengths",
                []
            )[:3],

            "areas_to_improve": data.get(
                "areas_to_improve",
                []
            )[:3],

            "suggestions": data.get(
                "suggestions",
                []
            )[:3],
        }

    except Exception as error:

        print(
            "ATS feedback generation failed:",
            error
        )

        return {
            "strengths": [],
            "areas_to_improve": [],
            "suggestions": [
                "Review the missing skills against the job description.",
                "Add measurable achievements where possible.",
                "Highlight projects that are most relevant to the target role.",
            ],
        }


# ---------------------------------------------------------
# Main ATS analysis
# ---------------------------------------------------------

def analyze_resume_against_job(
    resume_id: str,
    job_description: str
):

    resume_text = get_resume_text(
        resume_id
    )

    if not resume_text.strip():
        raise ValueError(
            "Resume content could not be extracted."
        )

    if not job_description.strip():
        raise ValueError(
            "Job description is empty."
        )

    analysis = calculate_ats_score(
        resume_text=resume_text,
        job_description=job_description
    )

    feedback = generate_ats_feedback(
        resume_text=resume_text,
        job_description=job_description,
        analysis=analysis
    )

    return {
        **analysis,
        "feedback": feedback,
    }