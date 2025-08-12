from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/liveness")
def liveness_check():
    return {"status": "alive"}

@app.get("/readiness")
def readiness_check():
    # Put actual readiness logic here (e.g., DB connection check)
    return {"status": "ready"}

if __name__ == "__main__":
    uvicorn.run("liveness_check:app", host="0.0.0.0", port=8000, reload=True)
