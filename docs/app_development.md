# API STEPS

### 1. Create virtual enviroment
```sh
python -m venv venv
```

### 2. Activate virtual enviroment
```sh
# on windows
.venv\scripts\activate.ps
# on unix sh shells
source venv/bin/activate
```

> How to deactivate my virtual enviroment? run the next command:
```sh
# on windows
venv/scripts/deactivate.ps
# on unix or sh
deactivate
```

### 3. Install FastAPI

Run the next command to install de module

```sh
pip install "fastapi[standard]"
```

### 4. Install SQLAlchemy to manage data with kind practices

Run the next command to install de module:

```sh
pip install SQLAlchemy
```

### 5. Create `requirements.txt` file
```sh
pip freeze > requirements.txt
```

### 6. Create `.gitignore` file and build it with Python options from [Toptal](https://www.toptal.com/developers/gitignore)
- Search and select `python`, `windows`, `linux`

### 7. Create packages `/config`, `/models`, `/schemas`, `/routers`, `/services`.
> Remember that a package has a `__init__.py` file

### 8. Config database _(sqlite)_

create the `database.py` file at `/config`:

```python
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker

# set path of sqllite file
sqilte_file = "../database.sqlite"
# define base dir with path of current file
base_dir = os.path.dirname(os.path.realpath(__file__))
# define URL of database connection
database_url = f"sqlite:///{os.path.join(base_dir, sqilte_file)}"
# define engine
engine = create_engine(database_url, echo=True)
# define Session
Session = sessionmaker(bind = engine)
# define base to manage database
Base = declarative_base()

```

### 9. Create the `Subject` model:

```python
from config.database import Base
from sqlalchemy import Column, Integer, String

class Subject(Base):
    # define the table name
    __tablename__ = "subjects"

    # define the properties of model
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), unique=True)
    description = Column(String(300), nullable=True)
```

### 10. Create the `SubjectSchema` schema:

```python
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from config.database import Session

from models.Subject import Subject


class SubjectSchema(BaseModel):
    ### SCHEMA PROPERTIES
    
    id: Optional[int] = None
    name: str = Field(min_length=1, max_length=150)
    description: Optional[str] = Field(min_length=1, max_length=300)

    ### VALIDATORS

    @field_validator("name")
    def name_must_be_unique(cls, value: str) -> str:
        # get db session
        db = Session()
        result = db.query(Subject).filter(Subject.name == value).count()
        if result:
            raise ValueError("Name must be unique")
        return value

    ### SCHEMA EXAMPLE

    # define schema example
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Mathematics",
                "description": "Mathematics is the study of quantity, structure, change, and space."
            }
        }
```

### 11. Create the `SubjectService` service:

```python
from models.Subject import Subject


class SubjectService:
    def __init__(self, db) -> None:
        self.db =db

    def get_subjects(self):
        """
        Get all subjects
        :return:
            list[Subject]: a list of all subjects in the database
        """
        result = self.db.query(Subject).all()
        return result

    def get_subject(self, id):
        """
        Get subject by id
        :param id: The id of the resource
        :return: The subject fund
        """
        result = self.db.query(Subject).filter(Subject.id == id).first()
        return result

    def create(self, subject: Subject):
        """
        Create a new subject
        :param self: the current object
        :param subject: the model to be created
        :return:
        """
        # define new model
        new_subject = Subject(**subject.dict())
        # store in database
        self.db.add(new_subject)
        # commit changes
        self.db.commit()
        return

    def update(self, id: int, data: Subject):
        """
        Update a subject
        :param id: the id of the model
        :param data: the data to be updated on model
        :return:
        """
        # load model from database
        subject = self.db.query(Subject).filter(Subject.id == id).first()
        # set model data
        subject.name = data.name
        subject.description = data.description
        # commit changes
        self.db.commit()
        return

    def delete(self, subject: Subject):
        """
        Delete a subject
        :param subject: the model to be deleted
        :return:
        """
        self.db.delete(subject)
        self.db.commit()
        return
```

### 12. Create the `subject_router` router:

```python
from fastapi import APIRouter, Path
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import List

from config.database import Session
from schemas.SubjectSchema import SubjectSchema
from services.SubjectService import SubjectService

# define router
subject_router = APIRouter()

### ROUTES

@subject_router.get(
    '/subjects',
    tags=['subjects'],
    response_model=list[SubjectSchema],
    status_code=200
)
def get_subjects() -> List[SubjectSchema]:
    # init db session
    db = Session()
    # get all subjects
    data = SubjectService(db).get_subjects()
    # return response
    return JSONResponse(status_code=200, content=jsonable_encoder(data))

@subject_router.get(
    '/subjects/{id}',
    tags=['subjects'],
    response_model=SubjectSchema,
    status_code=200
)
def get_subject(id: int = Path(ge=1, le=2000)) -> SubjectSchema:
    # init db session
    db = Session()
    # get model
    data = SubjectService(db).get_subject(id)
    # return response
    if data:
        return JSONResponse(status_code=200, content=jsonable_encoder(data))
    else:
        return JSONResponse(status_code=404, content={'message': 'Resource not found'})


@subject_router.post(
    '/subjects',
    tags=['subjects'],
    response_model=dict,
    status_code=201
)
def create_subject(subject: SubjectSchema) -> dict:
    # init db session
    db = Session()
    # create model
    SubjectService(db).create(subject)
    # return response
    return JSONResponse(status_code=201, content={'message': 'Resource created successfully'})


@subject_router.put(
    '/subjects/{id}',
    tags=['subjects'],
    response_model=dict,
    status_code=200
)
def update_subject(id: int, subject: SubjectSchema) -> dict:
    # init db session
    db = Session()
    # load model from db
    model = SubjectService(db).get_subject(id)

    # if model not found
    if not model:
        return JSONResponse(status_code=404, content={'message': 'Resource not found'})

    # update model
    SubjectService(db).update(id, subject)

    # return success response
    return JSONResponse(status_code=200, content={'message': 'Resource updated successfully'})


@subject_router.delete(
    '/subjects/{id}',
    tags=['subjects'],
    response_model=dict,
    status_code=200
)
def delete_subject(id: int) -> dict:
    # init db session
    db = Session()
    # load model from db
    model = SubjectService(db).get_subject(id)

    # if model not found
    if not model:
        return JSONResponse(status_code=404, content={'message': 'Resource not found'})

    # delete model
    SubjectService(db).delete(model)

    # return success response
    return JSONResponse(status_code=200, content={'message': 'Resource deleted successfully'})
```

### 13. Create the `main.py` file to run app

```python
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
```

### 14. Run app in development mode

```bash
uvicorn main:app --reload
```