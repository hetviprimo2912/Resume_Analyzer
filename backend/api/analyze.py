from fastapi import APIRouter, HTTPException

from llm.service import generate_resume_answer
from pydantic import BaseModel

router = APIRouter(
    prefix="/analyze",
    tags=["Resume Analysis"]
)

class AnalyzeRequest(BaseModel):

    resume_id: str

    query: str

    top_k: int = 3
    
@router.post("/")
def analyze_resume(
    request: AnalyzeRequest
):
    """
    Search an indexed resume.
    """

    try:

        result = generate_resume_answer(

            resume_id=request.resume_id,

            question=request.query,

            top_k=request.top_k
        )

        return {

            "success": True,

            "answer": result["answer"],

            "confidence": result["confidence"],

            "sources": [

                {

                    "section": item["chunk"].section,

                    "subsection": item["chunk"].subsection,

                    "page": item["chunk"].page,

                    "preview": (
                        item["chunk"].content[:180] + "..."
                        if len(item["chunk"].content) > 180
                        else item["chunk"].content
                    )

                }

                for item in result["matches"]

            ]

        }

    except FileNotFoundError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )