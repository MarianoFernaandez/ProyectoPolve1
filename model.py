# models.py
from pydantic import BaseModel
from typing import List
from datetime import date

class AlumnoModel(BaseModel):
    idalumno: int = None
    apyn: str
    idcurso: int
    curso: str = None
    fecnac: date

    class Config:
        from_attributes = True
        json_encoders = {
            date: lambda v: v.strftime('%Y-%m-%d')
        }

class CursoModel(BaseModel):
    idcurso: int = None
    curso: str

    class Config:
        from_attributes = True
