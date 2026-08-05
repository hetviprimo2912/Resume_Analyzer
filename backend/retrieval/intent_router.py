from enum import Enum


class ResumeSection(Enum):

    GENERAL = "GENERAL"

    PROJECTS = "PROJECTS"

    SKILLS = "SKILLS"

    EDUCATION = "EDUCATION"

    CONTACT = "CONTACT"

    ABOUT = "ABOUT"

SECTION_KEYWORDS = {

    ResumeSection.PROJECTS: [
        "project",
        "projects",
        "built",
        "developed",
        "development",
        "application",
        "applications",
        "app",
        "portfolio"
    ],

    ResumeSection.SKILLS: [
        "skill",
        "skills",
        "technology",
        "technologies",
        "framework",
        "frameworks",
        "language",
        "languages",
        "tech stack",
        "programming",
        "tools",
        "libraries"
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
        "master",
        "masters",
        "engineering",
    ],
    
    ResumeSection.CONTACT: [
        "contact",
        "phone",
        "mobile",
        "number",
        "email",
        "github",
        "linkedin",
        "address",
        "location"
    ],

    ResumeSection.ABOUT: [
        "about",
        "summary",
        "profile",
        "objective",
        "yourself",
        "introduction",
        "experience"
    ]
}

def detect_section(query: str) -> ResumeSection:
    """
    Detect which resume section the query is asking for.
    """

    query = query.lower()

    for section, keywords in SECTION_KEYWORDS.items():

        for keyword in keywords:

            if keyword in query:

                return section

    return ResumeSection.GENERAL