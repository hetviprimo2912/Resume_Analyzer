from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path

from services.resume_indexer import index_resume

router = APIRouter(
    prefix="/upload",
    tags=["Resume Upload"]
)


@router.post("/")
async def upload_resume(
    file: UploadFile = File(...)
):
    """
    Upload a resume and index it.
    """

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    upload_dir = Path("uploads")
    upload_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    file_path = upload_dir / file.filename

    with open(file_path, "wb") as buffer:
        buffer.write(
            await file.read()
        )

    resume_id = index_resume(
        str(file_path)
    )

    return {
        "success": True,
        "resume_id": resume_id,
        "message": "Resume indexed successfully."
    }