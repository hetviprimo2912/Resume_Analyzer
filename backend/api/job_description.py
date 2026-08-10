from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    HTTPException,
)

from parser.pdf_parser import extract_text_from_pdf

from services.ats_analyzer import (
    analyze_resume_against_job
)


router = APIRouter(
    prefix="/job-description",
    tags=["Job Description"]
)


@router.post("/analyze")
async def analyze_job_description(
    resume_id: str = Form(...),
    job_description: str = Form(""),
    file: UploadFile | None = File(None),
):
    """
    Analyze a resume against a pasted or uploaded
    job description.
    """

    # --------------------------------------------------
    # Get JD from uploaded PDF if provided
    # --------------------------------------------------

    if file is not None:

        if not file.filename.lower().endswith(".pdf"):

            raise HTTPException(
                status_code=400,
                detail="Only PDF job descriptions are supported."
            )

        pdf_bytes = await file.read()

        temp_path = (
            f"uploads/jd_{resume_id}.pdf"
        )

        try:

            with open(
                temp_path,
                "wb"
            ) as buffer:

                buffer.write(
                    pdf_bytes
                )

            parsed = extract_text_from_pdf(
                temp_path
            )

            job_description = parsed.get(
                "text",
                ""
            )

        except Exception as error:

            raise HTTPException(
                status_code=400,
                detail=f"Failed to read job description PDF: {error}"
            )

    # --------------------------------------------------
    # Validate JD
    # --------------------------------------------------

    job_description = (
        job_description or ""
    ).strip()
    print("\n========== JOB DESCRIPTION ==========")
    print(job_description)
    print("=====================================\n")
    if not job_description:

        raise HTTPException(
            status_code=400,
            detail="Please provide a job description."
        )

    # --------------------------------------------------
    # Analyze
    # --------------------------------------------------

    try:

        result = analyze_resume_against_job(
            resume_id=resume_id,
            job_description=job_description,
        )

        return {
            "success": True,
            **result,
        }

    except FileNotFoundError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:

        print(
            "JD analysis error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to analyze resume against job description."
        )