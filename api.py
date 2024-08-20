from datetime import date
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from sqlalchemy.orm import sessionmaker
from main import Alumno, Curso, engine
from model import AlumnoModel, CursoModel

app = FastAPI()

# CORS (permite la interacción con los navegadores)
origins = [
    "http://localhost",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint GET para obtener todos los alumnos en formato JSON
@app.get("/alumnos/", response_model=List[AlumnoModel])
def obtener_alumnos():
    alumnos_con_curso = Alumno.mostrar_todos()
    return alumnos_con_curso

# Endpoint POST para manejar el envío del formulario y crear un nuevo alumno
@app.post("/alumnos/nuevo/")
def agregar_alumno(alumno: AlumnoModel):
    try:
        alumno_agregado = Alumno.agregar_alumno(
            apyn=alumno.apyn,
            idcurso=alumno.idcurso,
            fecnac=alumno.fecnac
        )
        return {"message": "Alumno creado exitosamente", "alumno": alumno_agregado}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint DELETE para eliminar un alumno
@app.delete("/alumnos/{alumno_id}")
def eliminar_alumno(alumno_id: int):
    if not Alumno.eliminar_alumno(alumno_id):
        raise HTTPException(status_code=404, detail=f"Alumno con id {alumno_id} no encontrado")
    return {"message": f"Alumno con id {alumno_id} eliminado correctamente"}

# Endpoint PUT para modificar un alumno
@app.put("/alumnos/{alumno_id}", response_model=AlumnoModel)
def api_modificar_alumno(alumno_id: int, alumno_in: AlumnoModel):
    try:
        return Alumno.modificar_alumno(alumno_id, alumno_in)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint POST para agregar un curso
@app.post("/cursos/nuevo/")
def agregar_curso(curso: CursoModel):
    nuevo_curso = Curso.agregar_curso(curso.curso)
    return {"message": "Curso agregado exitosamente", "curso": CursoModel.model_validate(nuevo_curso)}

# Endpoint GET para recuperar todos los cursos
@app.get("/cursos/", response_model=List[CursoModel])
def recuperar_cursos():
    cursos = Curso.recuperar_cursos()
    return cursos