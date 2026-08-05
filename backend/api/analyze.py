from fastapi import APIRouter, HTTPException

from services.resume_search import search_resume
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

        results = search_resume(

            resume_id=request.resume_id,

            query=request.query,

            top_k=request.top_k
        )

        return {
            "success": True,
            "matches": [

                {

                    "distance": result["distance"],

                    "section": result["chunk"].section,

                    "subsection": result["chunk"].subsection,

                    "content": result["chunk"].content,

                    "page": result["chunk"].page

                }

                for result in results

            ]
        }

    except FileNotFoundError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )