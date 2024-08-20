USE dbbackend;

CREATE TABLE cursos (
    idcurso INT PRIMARY KEY IDENTITY(1,1),
    curso NVARCHAR(100) NOT NULL
);

CREATE TABLE alumnos (
    idalumno INT PRIMARY KEY IDENTITY(1,1),
    apyn NVARCHAR(100) NOT NULL,
    idcurso INT NOT NULL,
    fecnac DATE NOT NULL,
    FOREIGN KEY (idcurso) REFERENCES cursos(idcurso)
);

INSERT INTO cursos (curso) VALUES ('Matemáticas');
INSERT INTO cursos (curso) VALUES ('Historia');
INSERT INTO cursos (curso) VALUES ('Biología');
INSERT INTO cursos (curso) VALUES ('Literatura');
INSERT INTO cursos (curso) VALUES ('Física');

INSERT INTO alumnos (apyn, idcurso, fecnac) VALUES ('Juan Pérez', 1, '2005-03-15');
INSERT INTO alumnos (apyn, idcurso, fecnac) VALUES ('María Gómez', 2, '2004-07-22');
INSERT INTO alumnos (apyn, idcurso, fecnac) VALUES ('Carlos López', 3, '2005-01-30');
INSERT INTO alumnos (apyn, idcurso, fecnac) VALUES ('Ana Torres', 4, '2005-11-12');
INSERT INTO alumnos (apyn, idcurso, fecnac) VALUES ('Lucía Martínez', 5, '2004-05-20');
