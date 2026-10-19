from app import db
from app.dominios.alojamientos.modelos import Alojamiento


class AlojamientoRepositorio:
    @staticmethod
    def guardar(alojamiento):
        db.session.add(alojamiento)
        db.session.commit()
        return alojamiento

    @staticmethod
    def listar():
        return db.session.query(Alojamiento).all()

    @staticmethod
    def obtener_por_id(alojamiento_id):
        return db.session.get(Alojamiento, alojamiento_id)

    @staticmethod
    def eliminar(alojamiento):
        db.session.delete(alojamiento)
        db.session.commit()