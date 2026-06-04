from fastapi import FastAPI

from app.api.auth.router import router as auth_router

app = FastAPI(
    title="Enterprise Knowledge Assistant",
    description="Multi-tenant enterprise knowledge platform",
    version="0.1.0",
)

app.include_router(auth_router, prefix="/api/v1")


@app.get("/health")
def health():
    return {"status": "ok"}
