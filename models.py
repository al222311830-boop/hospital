from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

class Paciente(Base):

    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)

    nombre = Column(String(100), nullable=False)

    edad = Column(Integer, nullable=False)

    sexo = Column(String(20))

    diagnostico = Column(String(255))

    fecha_ingreso = Column(
        DateTime,
        server_default=func.now()
    )

    habitacion = Column(String(20))

    medico = Column(String(100))

    estado = Column(
        String(20),
        default="urgencias"
    )