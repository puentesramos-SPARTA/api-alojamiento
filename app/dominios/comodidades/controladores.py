from flask import Blueprint, request

from app.dominios.comodidades.dtos import CrearComodidadDTO
from app.seguridad import requiere_admin


comodidades_bp = Blueprint("comodidades", __name__)
comodidad_servicio = None


@comodidades_bp.post("")
@requiere_admin
def crear(usuario_id):
    datos = CrearComodidadDTO().load(
        request.get_json(silent=True) or {}
    )
    comodidad = comodidad_servicio.crear(datos)
    return {"success": True, "data": comodidad.to_dict()}, 201


@comodidades_bp.get("")
def listar():
    return {"success": True, "data": comodidad_servicio.listar()}, 200