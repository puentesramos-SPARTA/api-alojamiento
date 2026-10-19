from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError

from app.config import Config
from app.errores import ErrorAPI

API_VERSION = "v1"

db = SQLAlchemy()
migrate = Migrate()


def create_app(configuracion=None):
    """Crea y configura la aplicación Flask."""
    app = Flask(__name__)
    app.config.from_object(Config)

    if configuracion:
        app.config.update(configuracion)

    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, origins=app.config["CORS_ALLOWED_ORIGINS"])

    @app.get("/health")
    def health():
        return {
            "status": "ok",
            "service": "alojamientos-api",
            "version": API_VERSION,
        }, 200

    # Modelos acumulados para SQLAlchemy y Alembic.
    from app.dominios.usuarios import modelos as usuarios_modelos  # noqa: F401
    from app.dominios.alojamientos import modelos as alojamientos_modelos  # noqa: F401
    from app.dominios.comodidades import modelos as comodidades_modelos  # noqa: F401

    # Dominio Usuarios — Sprint 2.
    from app.dominios.usuarios import controladores as usuarios_ctrl
    from app.dominios.usuarios.controladores import admin_bp, usuarios_bp
    from app.dominios.usuarios.servicios import UsuarioServicio

    usuarios_ctrl.usuario_servicio = UsuarioServicio(
        app.config["SECRET_KEY"],
        app.config["JWT_EXP_MINUTES"],
    )

    app.register_blueprint(
        usuarios_bp,
        url_prefix=f"/api/{API_VERSION}/usuarios",
    )
    app.register_blueprint(
        admin_bp,
        url_prefix=f"/api/{API_VERSION}/admin",
    )

    # Dominio Alojamientos — Sprint 3.
    from app.dominios.alojamientos import controladores as alojamientos_ctrl
    from app.dominios.alojamientos.controladores import alojamientos_bp
    from app.dominios.alojamientos.servicios import AlojamientoServicio

    alojamientos_ctrl.alojamiento_servicio = AlojamientoServicio()
    app.register_blueprint(
        alojamientos_bp,
        url_prefix=f"/api/{API_VERSION}/alojamientos",
    )

    # Dominio Comodidades — Sprint 3.
    from app.dominios.comodidades import controladores as comodidades_ctrl
    from app.dominios.comodidades.controladores import comodidades_bp
    from app.dominios.comodidades.servicios import ComodidadServicio

    comodidades_ctrl.comodidad_servicio = ComodidadServicio()
    app.register_blueprint(
        comodidades_bp,
        url_prefix=f"/api/{API_VERSION}/comodidades",
    )

    @app.errorhandler(ValidationError)
    def manejar_error_validacion(error):
        return {
            "success": False,
            "error": {
                "message": "Datos inválidos.",
                "details": error.messages,
            },
        }, 400

    @app.errorhandler(ErrorAPI)
    def manejar_error_api(error):
        return {
            "success": False,
            "error": {"message": str(error)},
        }, error.status_code

    return app