from enum import Enum


class ResumeSection(Enum):

    GENERAL = "GENERAL"

    IDENTITY = "IDENTITY"

    PROJECTS = "PROJECTS"

    SKILLS = "SKILLS"

    EDUCATION = "EDUCATION"

    CONTACT = "CONTACT"

    EMAIL = "EMAIL"

    PHONE = "PHONE"

    LINKEDIN = "LINKEDIN"

    GITHUB = "GITHUB"

    ADDRESS = "ADDRESS"

    ABOUT = "ABOUT"


SECTION_KEYWORDS = {

    ResumeSection.IDENTITY: [
        "name",
        "full name",
        "candidate name",
        "who is the candidate",
        "who is this candidate",
        "candidate's name",
        "candidates name",
        "tell me the name",
        "tell me their name",
        "what is their name",
    ],

    ResumeSection.PROJECTS: [
        "project",
        "projects",
        "built",
        "developed",
        "development",
        "application",
        "applications",
        "app",
        "apps",
        "portfolio",
    ],

    ResumeSection.SKILLS: [
        "skill",
        "skills",
        "technical skill",
        "technical skills",
        "technology",
        "technologies",
        "framework",
        "frameworks",
        "programming language",
        "programming languages",
        "language",
        "languages",
        "tech stack",
        "programming",
        "tools",
        "libraries",
        "library",
        "database",
        "databases",
    ],

    ResumeSection.EDUCATION: [
        "education",
        "college",
        "university",
        "school",
        "degree",
        "cgpa",
        "gpa",
        "spi",
        "study",
        "studied",
        "graduate",
        "graduation",
        "bachelor",
        "bachelors",
        "master",
        "masters",
        "engineering",
        "semester",
        "academic",
    ],

    ResumeSection.EMAIL: [
        "email",
        "email address",
        "mail",
        "email id",
        "mail id",
    ],

    ResumeSection.PHONE: [
        "phone",
        "phone number",
        "mobile",
        "mobile number",
        "contact number",
        "telephone",
    ],

    ResumeSection.LINKEDIN: [
        "linkedin",
        "linkedin profile",
        "linkedin url",
    ],

    ResumeSection.GITHUB: [
        "github",
        "github profile",
        "github url",
    ],

    ResumeSection.ADDRESS: [
        "address",
        "location",
        "where does the candidate live",
        "where is the candidate from",
    ],

    ResumeSection.CONTACT: [
        "contact",
        "contact information",
        "contact details",
    ],

    ResumeSection.ABOUT: [
        "about",
        "summary",
        "profile",
        "objective",
        "yourself",
        "introduction",
        "experience",
        "background",
        "bio",
        "professional summary",
    ],
}


def detect_section(
    query: str,
    chunks=None
) -> ResumeSection:
    """
    Detect the most relevant resume section.

    Project names are checked first so that queries like:

        "Tell me about EcoGuard"

    are classified as PROJECTS instead of ABOUT.
    """

    query = query.lower().strip()

    if not query:
        return ResumeSection.GENERAL

    # =========================================================
    # 1. CHECK PROJECT NAMES FIRST
    # =========================================================

    if chunks:

        for chunk in chunks:

            chunk_section = (
                chunk.section
                .replace(" ", "")
                .upper()
            )

            if chunk_section != "PROJECTS":
                continue

            if not chunk.subsection:
                continue

            project_name = chunk.subsection.lower().strip()

            # Example:
            # "ECOGUARD :(ML Full Stack)"
            #
            # We only need the actual project name.
            project_name = project_name.split(":")[0].strip()

            if not project_name:
                continue

            if project_name in query:

                return ResumeSection.PROJECTS

    # =========================================================
    # 2. SPECIFIC CONTACT FIELDS
    # =========================================================

    if (
        "email" in query
        or "mail id" in query
        or "email id" in query
        or "email address" in query
    ):
        return ResumeSection.EMAIL

    if (
        "phone" in query
        or "mobile" in query
        or "telephone" in query
        or "contact number" in query
    ):
        return ResumeSection.PHONE

    if "linkedin" in query:
        return ResumeSection.LINKEDIN

    if "github" in query:
        return ResumeSection.GITHUB

    if (
        "address" in query
        or "location" in query
        or "where does the candidate live" in query
        or "where is the candidate from" in query
    ):
        return ResumeSection.ADDRESS

    # =========================================================
    # 3. CANDIDATE NAME
    # =========================================================

    identity_patterns = [
        "what is the candidate's name",
        "what is the candidates name",
        "what is the candidate name",
        "what's the candidate's name",
        "what's the candidates name",
        "candidate name",
        "full name",
        "who is the candidate",
        "who is this candidate",
        "tell me the candidate's name",
        "tell me the candidates name",
        "tell me their name",
        "what is their name",
    ]

    for pattern in identity_patterns:

        if pattern in query:

            return ResumeSection.IDENTITY

    # =========================================================
    # 4. EXPLICIT PROJECT QUESTIONS
    # =========================================================

    project_keywords = [
        "project",
        "projects",
        "built",
        "developed",
        "development",
        "application",
        "applications",
        "app",
        "apps",
        "portfolio",
    ]

    if any(
        keyword in query
        for keyword in project_keywords
    ):

        return ResumeSection.PROJECTS

    # =========================================================
    # 5. SKILLS
    # =========================================================

    skill_keywords = [
        "skill",
        "skills",
        "technical skill",
        "technical skills",
        "technology",
        "technologies",
        "framework",
        "frameworks",
        "programming language",
        "programming languages",
        "tech stack",
        "programming",
        "tools",
        "libraries",
        "library",
        "database",
        "databases",
    ]

    if any(
        keyword in query
        for keyword in skill_keywords
    ):

        return ResumeSection.SKILLS

    # =========================================================
    # 6. EDUCATION
    # =========================================================

    education_keywords = [
        "education",
        "college",
        "university",
        "school",
        "degree",
        "cgpa",
        "gpa",
        "spi",
        "study",
        "studied",
        "graduate",
        "graduation",
        "bachelor",
        "bachelors",
        "master",
        "masters",
        "engineering",
        "semester",
        "academic",
    ]

    if any(
        keyword in query
        for keyword in education_keywords
    ):

        return ResumeSection.EDUCATION

    # =========================================================
    # 7. ABOUT
    #
    # IMPORTANT:
    # Do NOT use "about" by itself here.
    #
    # Otherwise:
    # "Tell me about EcoGuard"
    #
    # would incorrectly become ABOUT.
    # =========================================================

    about_patterns = [
        "about the candidate",
        "about candidate",
        "about yourself",
        "tell me about the candidate",
        "tell me about candidate",
        "candidate profile",
        "candidate summary",
        "professional summary",
        "profile",
        "objective",
        "introduction",
        "background",
        "bio",
        "experience",
    ]

    if any(
        pattern in query
        for pattern in about_patterns
    ):

        return ResumeSection.ABOUT

    # =========================================================
    # 8. GENERAL
    # =========================================================

    return ResumeSection.GENERAL