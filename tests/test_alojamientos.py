def datos_alojamiento(titulo="Apartamento centro"):
    return {
        "titulo": titulo,
        "descripcion": "Alojamiento de prueba",
        "precio_noche": 180000,
        "ciudad": "Medellín",
    }


def crear_alojamiento(client, headers, titulo="Apartamento centro"):
    respuesta = client.post(
        "/api/v1/alojamientos",
        json=datos_alojamiento(titulo),
        headers=headers,
    )
    return respuesta.get_json()["data"]


def test_crear_alojamiento_asigna_propietario(client, usuario_auth):
    respuesta = client.post(
        "/api/v1/alojamientos",
        json=datos_alojamiento(),
        headers=usuario_auth,
    )

    assert respuesta.status_code == 201
    assert respuesta.get_json()["data"]["usuario_id"] is not None


def test_crear_alojamiento_sin_token(client):
    respuesta = client.post(
        "/api/v1/alojamientos",
        json=datos_alojamiento(),
    )

    assert respuesta.status_code == 401


def test_listar_alojamientos_es_publico(client):
    respuesta = client.get("/api/v1/alojamientos")

    assert respuesta.status_code == 200
    assert isinstance(respuesta.get_json()["data"], list)


def test_detalle_inexistente_devuelve_404(client):
    respuesta = client.get("/api/v1/alojamientos/999999")

    assert respuesta.status_code == 404


def test_propietario_actualiza_su_alojamiento(client, usuario_auth):
    alojamiento = crear_alojamiento(client, usuario_auth, "Propio")

    respuesta = client.patch(
        f"/api/v1/alojamientos/{alojamiento['id']}",
        json={"ciudad": "Bogotá"},
        headers=usuario_auth,
    )

    assert respuesta.status_code == 200
    assert respuesta.get_json()["data"]["ciudad"] == "Bogotá"


def test_usuario_no_actualiza_alojamiento_ajeno(
    client,
    usuario_auth,
    usuario_auth2,
):
    alojamiento = crear_alojamiento(client, usuario_auth, "Ajeno")

    respuesta = client.patch(
        f"/api/v1/alojamientos/{alojamiento['id']}",
        json={"ciudad": "Cali"},
        headers=usuario_auth2,
    )

    assert respuesta.status_code == 403


def test_admin_actualiza_alojamiento_ajeno(
    client,
    usuario_auth,
    admin_auth,
):
    alojamiento = crear_alojamiento(client, usuario_auth, "Administrable")

    respuesta = client.patch(
        f"/api/v1/alojamientos/{alojamiento['id']}",
        json={"ciudad": "Cartagena"},
        headers=admin_auth,
    )

    assert respuesta.status_code == 200
    assert respuesta.get_json()["data"]["ciudad"] == "Cartagena"


def test_propietario_elimina_su_alojamiento(client, usuario_auth):
    alojamiento = crear_alojamiento(client, usuario_auth, "Eliminar")

    respuesta = client.delete(
        f"/api/v1/alojamientos/{alojamiento['id']}",
        headers=usuario_auth,
    )

    assert respuesta.status_code == 204