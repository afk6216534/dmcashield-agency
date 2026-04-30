#!/usr/bin/env python3
"""
Minimal DMCAShield API - For HostingGuru Deployment
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="DMCAShield API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "ok", "service": "DMCAShield"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/api/status")
async def status():
    return {
        "status": "operational",
        "leads": 0,
        "tasks": 0
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)