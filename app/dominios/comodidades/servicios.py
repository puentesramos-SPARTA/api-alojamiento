from app.dominios.comodidades.modelos import Comodidad
from app.dominios.comodidades.repositorios import ComodidadRepositorio
from app.errores import ErrorAPI


class ComodidadServicio:
    def crear(self, datos):
        nombre = datos["nombre"].strip()

        if ComodidadRepositorio.obtener_por_nombre(nombre):
            raise ErrorAPI("La comodidad ya existe.", 409)

        comodidad = Comodidad(nombre=nombre)
        return ComodidadRepositorio.guardar(comodidad)

    def listar(self):
        return [
            comodidad.to_dict()
            for comodidad in ComodidadRepositorio.listar()
        ]