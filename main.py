from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine
from routers import buses, eta, carbon

# Create DB tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(buses.router)
app.include_router(eta.router)
app.include_router(carbon.router)

@app.get("/")
def root():
    return {"message": "Backend is running 🚍"}
