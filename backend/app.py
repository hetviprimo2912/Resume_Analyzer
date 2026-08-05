from fastapi import FastAPI

from api.upload import router as upload_router
from api.analyze import router as analyze_router


app = FastAPI(
    title="AI Resume Analyzer API",
    version="1.0.0"
)

app.include_router(upload_router)
app.include_router(analyze_router)


@app.get("/")
def root():

    return {
        "message": "AI Resume Analyzer Backend Running 🚀"
    }