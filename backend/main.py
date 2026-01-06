"""
FastAPI Main Application
Entry point for the ATS Resume Optimization System backend.
"""

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional, Any
import uvicorn
from datetime import datetime
import numpy as np

from resume_parser import ResumeParser
from ats_engine import ATSEngine


def convert_to_serializable(obj: Any) -> Any:
    """Convert numpy types to Python native types for JSON serialization"""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {key: convert_to_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_serializable(item) for item in obj]
    return obj


# Initialize FastAPI app
app = FastAPI(
    title="ATS Resume Optimization System",
    description="Analyze resumes against job descriptions and get ATS scores",
    version="1.0.0"
)

# Configure CORS for frontend access (allow any localhost port)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
resume_parser = ResumeParser()
ats_engine = ATSEngine()


@app.get("/")
async def root():
    """
    Root endpoint - Health check and API information.
    """
    return {
        "message": "ATS Resume Optimization System API",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "analyze": "/analyze",
            "health": "/health",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(..., description="Resume file (PDF or DOCX)"),
    job_category: str = Form(..., description="Job category (IT or Non-IT)"),
    job_role: str = Form(..., description="Target job role"),
    experience_level: str = Form(..., description="Experience level (Fresher or Experienced)")
):
    """
    Main endpoint to analyze resume against job role and experience.

    Args:
        file: Uploaded resume file (PDF or DOCX)
        job_category: Job category ("IT" or "Non-IT")
        job_role: Target job role
        experience_level: Experience level ("Fresher" or "Experienced")

    Returns:
        JSON response with ATS analysis results

    Raises:
        HTTPException: On validation or processing errors
    """
    try:
        # Validate inputs
        if not file:
            raise HTTPException(
                status_code=400,
                detail="No file provided"
            )

        if not job_role or len(job_role.strip()) < 2:
            raise HTTPException(
                status_code=400,
                detail="Job role must be specified"
            )

        # Validate category
        valid_categories = ["IT", "Non-IT"]
        job_category = job_category.strip()
        if job_category not in valid_categories:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid category. Must be one of: {', '.join(valid_categories)}"
            )

        # Validate experience level
        valid_experience = ["Fresher", "Experienced"]
        experience_level = experience_level.strip()
        if experience_level not in valid_experience:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid experience level. Must be one of: {', '.join(valid_experience)}"
            )

        # Validate file size (max 10MB)
        file_content = await file.read()
        file_size_mb = len(file_content) / (1024 * 1024)
        if file_size_mb > 10:
            raise HTTPException(
                status_code=400,
                detail="File size exceeds 10MB limit"
            )

        # Reset file pointer and create a new UploadFile-like object
        from io import BytesIO
        from fastapi import UploadFile as FastAPIUploadFile

        file_buffer = BytesIO(file_content)
        file_buffer.name = file.filename
        upload_file = FastAPIUploadFile(
            filename=file.filename,
            file=file_buffer
        )

        # Step 1: Parse the resume
        parsed_resume = resume_parser.parse_file(upload_file)

        # Step 2: Run ATS analysis
        analysis_result = ats_engine.analyze(
            resume_text=parsed_resume["cleaned_text"],
            job_role=job_role,
            job_category=job_category,
            experience_level=experience_level
        )

        # Convert numpy types to native Python types for JSON serialization
        analysis_result = convert_to_serializable(analysis_result)
        parsed_resume = convert_to_serializable(parsed_resume)

        # Step 3: Prepare response
        response = {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "file_info": {
                "filename": parsed_resume["filename"],
                "file_type": parsed_resume["file_type"],
                "word_count": parsed_resume["word_count"]
            },
            "analysis": {
                "overall_score": analysis_result["overall_score"],
                "verdict": analysis_result["verdict"],
                "breakdown": analysis_result["breakdown"],
                "matched_keywords": analysis_result["matched_keywords"],
                "missing_keywords": analysis_result["missing_keywords"],
                "recommendations": analysis_result["recommendations"],
                "job_category": analysis_result["job_category"],
                "job_role": analysis_result["job_role"],
                "experience_level": analysis_result["experience_level"],
                "summary_analysis": analysis_result.get("summary_analysis", {})
            }
        }

        # Final conversion to ensure all nested numpy types are converted
        response = convert_to_serializable(response)

        return JSONResponse(content=response, status_code=200)

    except HTTPException:
        raise
    except Exception as e:
        # Log the error (in production, use proper logging)
        print(f"Error in analyze_resume: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing your request: {str(e)}"
        )


@app.post("/test-parse")
async def test_parse_resume(file: UploadFile = File(...)):
    """
    Test endpoint to only parse resume without analysis.
    Useful for debugging and testing resume extraction.

    Args:
        file: Uploaded resume file (PDF or DOCX)

    Returns:
        JSON response with parsed resume data
    """
    try:
        parsed_resume = resume_parser.parse_file(file)

        # Extract contact info
        email = resume_parser.extract_email(parsed_resume["cleaned_text"])
        phone = resume_parser.extract_phone(parsed_resume["cleaned_text"])

        return {
            "success": True,
            "filename": parsed_resume["filename"],
            "file_type": parsed_resume["file_type"],
            "word_count": parsed_resume["word_count"],
            "character_count": parsed_resume["character_count"],
            "email": email,
            "phone": phone,
            "preview": parsed_resume["cleaned_text"][:500] + "..."  # First 500 chars
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error parsing resume: {str(e)}"
        )


@app.exception_handler(404)
async def not_found_handler(request, exc):
    """
    Custom 404 handler.
    """
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "error": "Endpoint not found",
            "message": "The requested endpoint does not exist"
        }
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """
    Custom 500 handler.
    """
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "message": "An unexpected error occurred"
        }
    )


# Run the application
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload for development
        log_level="info"
    )
