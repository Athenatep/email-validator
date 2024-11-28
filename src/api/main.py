from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from typing import List, Optional
import logging
from .models import (
    EmailValidationRequest,
    EmailValidationResponse,
    BatchValidationRequest,
    BatchValidationResponse,
    ValidationOptions,
    CacheStats,
    ReportRequest
)
from ..validators.email_validator import EmailValidator
from ..preprocessing.preprocessor import EmailPreprocessor
from ..cache.cache_manager import CacheManager
from ..visualization.report_generator import ReportGenerator

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Email Validator API",
    description="REST API for comprehensive email validation",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
validator = EmailValidator(cache_enabled=True)
preprocessor = EmailPreprocessor()
cache_manager = CacheManager()
report_generator = ReportGenerator()

@app.get("/")
async def root():
    """API health check endpoint."""
    return {"status": "healthy", "service": "Email Validator API"}

@app.post("/validate", response_model=EmailValidationResponse)
async def validate_email(request: EmailValidationRequest):
    """
    Validate a single email address.
    
    Args:
        request: Email validation request
        
    Returns:
        Validation results
    """
    try:
        results = await validator.validate(
            request.email,
            request.options.dict() if request.options else None
        )
        return EmailValidationResponse(**results)
    except Exception as e:
        logger.error(f"Error validating email: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/validate/batch", response_model=BatchValidationResponse)
async def validate_batch(request: BatchValidationRequest):
    """
    Validate a batch of email addresses.
    
    Args:
        request: Batch validation request
        
    Returns:
        Batch validation results
    """
    try:
        # Preprocess emails
        preprocess_results = await preprocessor.preprocess(request.emails)
        
        # Validate each email
        validation_results = []
        for email in preprocess_results["processed_emails"]:
            result = await validator.validate(
                email,
                request.options.dict() if request.options else None
            )
            validation_results.append(result)
            
        return BatchValidationResponse(
            results=validation_results,
            stats=preprocess_results["stats"],
            invalid_format=preprocess_results["invalid_format"],
            duplicates=preprocess_results["duplicates"]
        )
    except Exception as e:
        logger.error(f"Error in batch validation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/report")
async def generate_report(request: ReportRequest):
    """
    Generate validation report with visualizations.
    
    Args:
        request: Report generation request
        
    Returns:
        Path to generated report
    """
    try:
        report_path = await report_generator.generate_report(
            request.results,
            request.format
        )
        
        if not report_path:
            raise HTTPException(
                status_code=500,
                detail="Error generating report"
            )
            
        return FileResponse(
            report_path,
            media_type="text/html" if request.format == "html" else "application/pdf",
            filename=report_path.split("/")[-1]
        )
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/cache/stats", response_model=CacheStats)
async def get_cache_stats():
    """Get cache statistics."""
    try:
        stats = await cache_manager.get_stats()
        return CacheStats(**stats)
    except Exception as e:
        logger.error(f"Error getting cache stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/cache/clear")
async def clear_cache():
    """Clear expired cache entries."""
    try:
        await cache_manager.clear()
        return {"status": "success", "message": "Cache cleared successfully"}
    except Exception as e:
        logger.error(f"Error clearing cache: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))