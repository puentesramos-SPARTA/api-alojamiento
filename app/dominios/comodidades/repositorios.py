from app import db
from app.dominios.comodidades.modelos import Comodidad


class ComodidadRepositorio:
    @staticmethod
    def guardar(comodidad):
        db.session.add(comodidad)
        db.session.commit()
        return comodidad

    @staticmethod
    def listar():
        return db.session.query(Comodidad).all()

    @staticmethod
    def obtener_por_nombre(nombre):
        return (
            db.session.query(Comodidad)
            .filter_by(nombre=nombre)
            .first()
        )

    @staticmethod
    def obtener_por_ids(ids):
        return (
            db.session.query(Comodidad)
            .filter(Comodidad.id.in_(ids))
            .all()
        )