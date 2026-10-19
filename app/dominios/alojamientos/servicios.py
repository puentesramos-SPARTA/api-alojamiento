from app.dominios.alojamientos.modelos import Alojamiento
from app.dominios.alojamientos.repositorios import AlojamientoRepositorio
from app.dominios.comodidades.repositorios import ComodidadRepositorio
from app.dominios.usuarios.repositorios import UsuarioRepositorio
from app.errores import ErrorAPI


class AlojamientoServicio:
    def crear(self, datos, usuario_id):
        alojamiento = Alojamiento(**datos, usuario_id=usuario_id)
        return AlojamientoRepositorio.guardar(alojamiento)

    def listar(self):
        return [
            alojamiento.to_dict()
            for alojamiento in AlojamientoRepositorio.listar()
        ]

    def obtener(self, alojamiento_id):
        alojamiento = AlojamientoRepositorio.obtener_por_id(alojamiento_id)
        if not alojamiento:
            raise ErrorAPI("Alojamiento no encontrado.", 404)
        return alojamiento

    def _validar_permiso(self, alojamiento, usuario_id):
        usuario = UsuarioRepositorio.obtener_por_id(usuario_id)
        es_admin = usuario is not None and usuario.rol == "admin"

        if alojamiento.usuario_id != usuario_id and not es_admin:
            raise ErrorAPI(
                "Solo el propietario o un administrador puede modificar "
                "el alojamiento.",
                403,
            )

    def actualizar(self, alojamiento_id, usuario_id, datos):
        alojamiento = self.obtener(alojamiento_id)
        self._validar_permiso(alojamiento, usuario_id)

        for campo, valor in datos.items():
            if valor is not None:
                setattr(alojamiento, campo, valor)

        return AlojamientoRepositorio.guardar(alojamiento)

    def eliminar(self, alojamiento_id, usuario_id):
        alojamiento = self.obtener(alojamiento_id)
        self._validar_permiso(alojamiento, usuario_id)
        AlojamientoRepositorio.eliminar(alojamiento)

    def asignar_comodidades(self, alojamiento_id, usuario_id, ids):
        alojamiento = self.obtener(alojamiento_id)
        self._validar_permiso(alojamiento, usuario_id)

        ids_unicos = set(ids)
        comodidades = (
            ComodidadRepositorio.obtener_por_ids(ids_unicos)
            if ids_unicos
            else []
        )

        if len(comodidades) != len(ids_unicos):
            raise ErrorAPI("Una o más comodidades no existen.", 400)

        alojamiento.comodidades = comodidades
        return AlojamientoRepositorio.guardar(alojamiento)