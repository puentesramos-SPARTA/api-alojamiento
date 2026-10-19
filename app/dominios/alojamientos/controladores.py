from flask import Blueprint, request

from app.dominios.alojamientos.dtos import (
    ActualizarAlojamientoDTO,
    CrearAlojamientoDTO,
)
from app.dominios.comodidades.dtos import AsignarComodidadesDTO
from app.seguridad import requiere_token


alojamientos_bp = Blueprint("alojamientos", __name__)
alojamiento_servicio = None


@alojamientos_bp.post("")
@requiere_token
def crear(usuario_id):
    datos = CrearAlojamientoDTO().load(
        request.get_json(silent=True) or {}
    )
    alojamiento = alojamiento_servicio.crear(datos, usuario_id)
    return {"success": True, "data": alojamiento.to_dict()}, 201


@alojamientos_bp.get("")
def listar():
    return {"success": True, "data": alojamiento_servicio.listar()}, 200


@alojamientos_bp.get("/<int:alojamiento_id>")
def detalle(alojamiento_id):
    alojamiento = alojamiento_servicio.obtener(alojamiento_id)
    return {"success": True, "data": alojamiento.to_dict()}, 200


@alojamientos_bp.patch("/<int:alojamiento_id>")
@requiere_token
def actualizar(usuario_id, alojamiento_id):
    datos = ActualizarAlojamientoDTO().load(
        request.get_json(silent=True) or {}
    )
    alojamiento = alojamiento_servicio.actualizar(
        alojamiento_id,
        usuario_id,
        datos,
    )
    return {"success": True, "data": alojamiento.to_dict()}, 200


@alojamientos_bp.delete("/<int:alojamiento_id>")
@requiere_token
def eliminar(usuario_id, alojamiento_id):
    alojamiento_servicio.eliminar(alojamiento_id, usuario_id)
    return "", 204


@alojamientos_bp.patch("/<int:alojamiento_id>/comodidades")
@requiere_token
def asignar_comodidades(usuario_id, alojamiento_id):
    datos = AsignarComodidadesDTO().load(
        request.get_json(silent=True) or {}
    )
    alojamiento = alojamiento_servicio.asignar_comodidades(
        alojamiento_id,
        usuario_id,
        datos["comodidades_ids"],
    )
    return {"success": True, "data": alojamiento.to_dict()}, 200