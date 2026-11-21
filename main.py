from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, get_db
from database import Base
from models import Paciente
from pydantic import BaseModel, Field
from typing import Optional, Literal

app = FastAPI(
    title="API Hospitalaria",
    description="Sistema de gestión de pacientes",
    version="1.0"
)

Base.metadata.create_all(bind=engine)


class PacienteCrear(BaseModel):
    nombre: str
    edad: int = Field(gt=0, le=120)
    sexo: Optional[str] = None
    diagnostico: Optional[str] = None
    habitacion: Optional[str] = None
    medico: Optional[str] = None
    estado: Literal["alta", "urgencias", "piso", "reposo"] = "urgencias"


class CambiarEstado(BaseModel):
    estado: Literal["alta", "urgencias", "piso", "reposo"]


@app.get("/")
def inicio():
    return {
        "mensaje": "API del Hospital funcionando correctamente"
    }


# REGISTRAR PACIENTE
@app.post("/pacientes")
def registrar_paciente(
    datos: PacienteCrear,
    db: Session = Depends(get_db)
):

    paciente = Paciente(**datos.model_dump())

    db.add(paciente)
    db.commit()
    db.refresh(paciente)

    return {
        "mensaje": "Paciente registrado correctamente",
        "paciente": paciente.id
    }


# MOSTRAR TODOS LOS PACIENTES
@app.get("/pacientes")
def mostrar_pacientes(db: Session = Depends(get_db)):

    return db.query(Paciente).all()


# BUSCAR PACIENTE POR ID
@app.get("/pacientes/{id}")
def buscar_paciente(
    id: int,
    db: Session = Depends(get_db)
):

    paciente = db.query(Paciente).filter(
        Paciente.id == id
    ).first()

    if not paciente:
        raise HTTPException(404, "Paciente no encontrado")

    return paciente


# FILTRAR PACIENTES POR ESTADO
@app.get("/pacientes/estado/{estado}")
def pacientes_por_estado(
    estado: Literal["alta", "urgencias", "piso", "reposo"],
    db: Session = Depends(get_db)
):

    return db.query(Paciente).filter(
        Paciente.estado == estado
    ).all()


# CAMBIAR ESTADO DEL PACIENTE
@app.put("/pacientes/{id}/estado")
def cambiar_estado(
    id: int,
    datos: CambiarEstado,
    db: Session = Depends(get_db)
):

    paciente = db.query(Paciente).filter(
        Paciente.id == id
    ).first()

    if not paciente:
        raise HTTPException(404, "Paciente no encontrado")

    paciente.estado = datos.estado

    db.commit()
    db.refresh(paciente)

    return {
        "mensaje": "Estado actualizado correctamente",
        "nuevo_estado": paciente.estado
    }


# ELIMINAR PACIENTE
@app.delete("/pacientes/{id}")
def eliminar_paciente(
    id: int,
    db: Session = Depends(get_db)
):

    paciente = db.query(Paciente).filter(
        Paciente.id == id
    ).first()

    if not paciente:
        raise HTTPException(404, "Paciente no encontrado")

    db.delete(paciente)
    db.commit()

    return {
        "mensaje": "Paciente eliminado correctamente"
    }


# CONTAR PACIENTES POR ESTADO
@app.get("/estadisticas")
def estadisticas(db: Session = Depends(get_db)):

    estados = ["alta", "urgencias", "piso", "reposo"]

    resultado = {}

    for estado in estados:

        cantidad = db.query(Paciente).filter(
            Paciente.estado == estado
        ).count()

        resultado[estado] = cantidad

    return resultado