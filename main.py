from fastapi import FastAPI
from config.database import Base, engine

# add routers here ->

# create app
app = FastAPI(debug=True)

### ROUTERS

### META
Base.metadata.create_all(bind=engine)

### ROUTES
@app.get("/")
def root():
    return {"message": "Hello World - Welcome to ClassTrackAPI"}