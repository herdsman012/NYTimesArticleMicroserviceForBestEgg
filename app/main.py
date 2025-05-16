from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()
from app.config import get_settings
from app.routes.nyt_routes import router as api_router

# Create FastAPI application
settings = get_settings()
print(settings)

# Configure CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: In release version, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router)


# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint that returns basic API information.
    """
    return {
        "message": "Welcome to the NYTimes Articles API",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
