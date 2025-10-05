"""
FastAPI main application for Panchangam Calendar API
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.routers import panchangam
from app.models.panchangam import PanchangamRequest, PanchangamResponse

# Create FastAPI app instance
app = FastAPI(
    title="Panchangam Calendar API",
    description="Accurate Panchangam calculations using Swiss Ephemeris",
    version="1.0.0"
)

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(panchangam.router, prefix="/api", tags=["panchangam"])

# Health check endpoint
@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Panchangam Calendar API is running", "status": "healthy"}

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "service": "Panchangam Calendar API",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)