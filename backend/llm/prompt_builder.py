def build_prompt(
    question: str,
    matches
):
    """
    Build the prompt that will be sent to the LLM.
    """

    context_parts = []

    for result in matches:

        chunk = result["chunk"]

        section = chunk.section.replace(" ", "").upper()

        SECTION_NAMES = {
            "ABOUTME": "ABOUT ME",
            "PROJECTS": "PROJECTS",
            "SKILLS": "SKILLS",
            "EDUCATION": "EDUCATION",
            "CONTACT": "CONTACT"
        }

        section = SECTION_NAMES.get(section, section)

        # -----------------------------------
        # PROJECT Section
        # -----------------------------------
        if section == "PROJECTS":

            content = chunk.content

            # Remove duplicated project title from the content
            if (
                chunk.subsection
                and content.startswith(chunk.subsection)
            ):
                content = content[len(chunk.subsection):].strip()

            context_parts.append(
f"""
Project Name:
{chunk.subsection}

Details:
{content}
"""
)
            

        # -----------------------------------
        # Other Sections
        # -----------------------------------
        else:

            context_parts.append(
f"""
==================================================

{section}

{chunk.content}
"""
            )

    context = "\n".join(context_parts)

    prompt = f"""
You are an expert AI Resume Analyzer.

You must answer ONLY using the resume context below.

--------------------------
STRICT RULES
--------------------------

1. NEVER invent information.

2. NEVER use outside knowledge.

3. Ignore any resume section that is unrelated to the user's question.

4. Answer ONLY what the user asked.

Examples:

Question:
What is the candidate's name?

Good Answer:
Hetvi Prajapati

Bad Answer:
Hetvi Prajapati has worked on ECOGUARD...

--------------------------

Question:
What projects has the candidate built?

Answer:
Only mention projects.

Do NOT mention education.

Do NOT mention skills.

Do NOT mention contact information.

--------------------------

Question:
Where did the candidate study?

Answer:
Only answer using the Education section.

--------------------------

Question:
What are the candidate's skills?

Answer:
Only answer using the Skills section.

--------------------------

If the answer does not exist in the resume, reply exactly:

I couldn't find that information in the resume.

--------------------------

Write naturally.

Do not write:

SECTION:
CONTENT:
PROJECT:

Do not copy resume formatting.

Summarize naturally like a professional assistant.

====================================================

RESUME CONTEXT

{context}

====================================================

USER QUESTION

{question}

ANSWER:
"""

    return prompt