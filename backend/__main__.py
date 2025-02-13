from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from backend.settings import Settings
from backend.shortener.views import router as shortener_router

settings = Settings()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.allowed_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.include_router(shortener_router)

@app.get("/health_check")
async def health_check():
    return {"status": "ok"}
