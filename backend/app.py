from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.upload import router as upload_router
from api.analyze import router as analyze_router
from api.job_description import router as job_description_router


app = FastAPI(
    title="AI Resume Analyzer API",
    version="1.0.0"
)

# -----------------------------
# Enable CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(analyze_router)
app.include_router(job_description_router)


@app.get("/")
def root():
    return {
        "message": "AI Resume Analyzer Backend Running 🚀"
    }