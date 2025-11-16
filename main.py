from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from osint_researcher import OSINTResearcher

# Load environment variables
load_dotenv()

app = FastAPI(title="OSINT Deep Research Application")

# Initialize OSINT Researcher
researcher = OSINTResearcher(api_key=os.getenv("OPENAI_API_KEY"))


class ResearchRequest(BaseModel):
    name: str
    details: str = ""


class ResearchResponse(BaseModel):
    status: str
    research_report: str
    metadata: dict


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main HTML page"""
    try:
        with open("static/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>OSINT Deep Research</h1><p>Frontend not found</p>")


@app.post("/api/research", response_model=ResearchResponse)
async def conduct_research(request: ResearchRequest):
    """
    Conduct deep OSINT research on a person
    """
    if not request.name or len(request.name.strip()) < 2:
        raise HTTPException(status_code=400, detail="Name must be at least 2 characters long")

    try:
        # Conduct OSINT research using o3-deep-research model
        result = await researcher.research_person(
            name=request.name,
            details=request.details
        )

        return ResearchResponse(
            status="success",
            research_report=result["report"],
            metadata=result["metadata"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Research failed: {str(e)}")


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "OSINT Deep Research",
        "model": "gpt-4-turbo-preview"
    }


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))

    print(f"Starting OSINT Deep Research Application on {host}:{port}")
    uvicorn.run(app, host=host, port=port)
