from fastapi import FastAPI
from . import models
from .database import engine
from .routers import workers, policies, claims
from .routers import premium
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GigShield AI Backend",
    description="API for parametric insurance tailored to gig workers.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(workers.router)
app.include_router(policies.router)
app.include_router(claims.router, prefix="/claims", tags=["Claims"])
app.include_router(premium.router, prefix="/premium", tags=["Premium"])

@app.get("/")
def root():
    return {"message": "Welcome to GigShield AI Backend"}