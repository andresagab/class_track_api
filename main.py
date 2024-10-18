from fastapi import FastAPI
from config.database import Base, engine

# add routers here ->
from routers.subject_router import subject_router

# create app
app = FastAPI(debug=True)

### ROUTERS
app.include_router(subject_router)

### META
Base.metadata.create_all(bind=engine)

### ROUTES
@app.get("/")
def root():
    return {"message": "Hello World - Welcome to ClassTrackAPI"}