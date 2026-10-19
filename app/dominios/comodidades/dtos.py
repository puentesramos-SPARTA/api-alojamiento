from marshmallow import Schema, fields, validate


class CrearComodidadDTO(Schema):
    nombre = fields.String(
        required=True,
        validate=validate.Length(min=1),
    )


class AsignarComodidadesDTO(Schema):
    comodidades_ids = fields.List(
        fields.Integer(strict=True),
        required=True,
    )