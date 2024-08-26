'''
instalado:
FastAPI (completo, incluido jinja2 y uvicorn)
sql server management estudio 20
sql server (evaluation version)
python 3.12.4 (64-bit)
pyodbc
SQLAlchemy
Microsoft ODBC Driver 18 for SQL Server (x64) version 18.3.3.1
Microsoft Visual C++ Redistributable (version 14.40.33810.0)
'''

from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, joinedload
from model import AlumnoModel, CursoModel  # Si es necesario
from fastapi import HTTPException

server = r'SQLSERVER\\SQLSERVER'
database = 'bdg1'
username = 'bdg1'
password = 'bdg1'

connection_string = (
    f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+18+for+SQL+Server'
    '&TrustServerCertificate=yes'
)

"""
# Pruebo la conexión
try:
    engine = create_engine(connection_string)
    print("Conexión exitosa!")
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")
"""

# Creo el motor de SQLAlchemy y declaro la clase base
engine = create_engine(connection_string)
Base = declarative_base()

# Defino la clase Alumno (en base a la tabla de la base de datos)
class Alumno(Base):
    __tablename__ = 'alumnos'

    idalumno = Column(Integer, primary_key=True, autoincrement=True)
    apyn = Column(String)
    idcurso = Column(Integer, ForeignKey('cursos.idcurso'))
    fecnac = Column(Date)

    # Relación con la tabla 'cursos'
    curso = relationship('Curso', back_populates='alumnos')

    @classmethod
    def mostrar_todos(cls):
        session = sessionmaker(bind=engine)()
        alumnos = session.query(cls).options(joinedload(cls.curso)).all()
        session.close()

        # Mapea los datos para incluir el nombre del curso
        alumnos_con_curso = [
            {
                "idalumno": alumno.idalumno,
                "apyn": alumno.apyn,
                "idcurso": alumno.idcurso,
                "curso": alumno.curso.curso,  # Aquí se obtiene el nombre del curso
                "fecnac": alumno.fecnac
            }
            for alumno in alumnos
        ]

        return alumnos_con_curso

    @classmethod
    def agregar_alumno(cls, apyn: str, idcurso: int, fecnac: Date):
        Session = sessionmaker(bind=engine)
        session = Session()

        # Obtener el curso correspondiente al idcurso proporcionado
        curso = session.query(Curso).filter(Curso.idcurso == idcurso).one_or_none()
        if not curso:
            session.close()
            raise Exception(f"Curso con id {idcurso} no encontrado")  # Manejo de errores más sencillo

        # Crear un nuevo alumno
        nuevo_alumno = cls(apyn=apyn, idcurso=idcurso, fecnac=fecnac)
        session.add(nuevo_alumno)
        session.commit()
        session.refresh(nuevo_alumno)

        # Obtener el nombre del curso
        nombre_curso = curso.curso
        session.close()

        # Crear el diccionario con la información del nuevo alumno
        alumno_con_curso = {
            "idalumno": nuevo_alumno.idalumno,
            "apyn": nuevo_alumno.apyn,
            "idcurso": nuevo_alumno.idcurso,
            "curso": nombre_curso,
            "fecnac": nuevo_alumno.fecnac
        }

        return alumno_con_curso
    
    @classmethod
    def eliminar_alumno(cls, alumno_id):
        session = sessionmaker(bind=engine)()
        alumno = session.query(cls).filter_by(idalumno=alumno_id).first()
        if alumno:
            session.delete(alumno)
            session.commit()
            session.close()
            return True
        session.close()
        return False
        
    @classmethod
    def modificar_alumno(cls, alumno_id: int, alumno_in: AlumnoModel):
        session = sessionmaker(bind=engine)()
        alumno_existente = session.query(cls).filter(cls.idalumno == alumno_id).one_or_none()
        if not alumno_existente:
            session.close()
            raise Exception(f"Alumno con id {alumno_id} no encontrado")
        alumno_existente.apyn = alumno_in.apyn
        alumno_existente.idcurso = alumno_in.idcurso
        alumno_existente.fecnac = alumno_in.fecnac
        
        session.commit()
        session.refresh(alumno_existente)
        
        curso = session.query(Curso).filter(Curso.idcurso == alumno_existente.idcurso).one_or_none()
        nombre_curso = curso.curso if curso else None
        session.close()
        alumno_con_curso = AlumnoModel(
            idalumno=alumno_existente.idalumno,
            apyn=alumno_existente.apyn,
            idcurso=alumno_existente.idcurso,
            curso=nombre_curso,
            fecnac=alumno_existente.fecnac
        )
        return alumno_con_curso

# Defino la clase Curso (en base a la tabla de la base de datos)
class Curso(Base):
    __tablename__ = 'cursos'

    idcurso = Column(Integer, primary_key=True, autoincrement=True)
    curso = Column(String)

    # Relación inversa
    alumnos = relationship('Alumno', back_populates='curso')

    
    @classmethod
    def agregar_curso(cls, curso):
        nuevo_curso = cls(
            curso=curso
        )
        session = sessionmaker(bind=engine)()
        session.add(nuevo_curso)
        session.commit()
        session.refresh(nuevo_curso)
        session.close()
        return nuevo_curso
    
    @classmethod
    def recuperar_cursos(cls):
        session = sessionmaker(bind=engine)()
        cursos = session.query(cls).all()
        session.close()
        return cursos