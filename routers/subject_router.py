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
    SubjectService(db).delete(id)

    # return success response
    return JSONResponse(status_code=200, content={'message': 'Resource deleted successfully'})