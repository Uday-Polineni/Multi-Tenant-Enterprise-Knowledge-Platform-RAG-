from fastapi import FastAPI

app = FastAPI(
    title="Enterprise Knowledge Assistant",
    description="Multi-tenant enterprise knowledge platform",
    version="0.1.0",
)


@app.get("/health")
def health():
    return {"status": "ok"}
