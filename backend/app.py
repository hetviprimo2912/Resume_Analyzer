from fastapi import FastAPI

app = FastAPI(
    title="AI Resume Analyzer API",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "AI Resume Analyzer Backend Running 🚀"
    }