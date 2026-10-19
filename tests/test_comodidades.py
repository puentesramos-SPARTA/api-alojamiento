def crear_alojamiento(client, headers, titulo="Casa"):
    respuesta = client.post(
        "/api/v1/alojamientos",
        json={
            "titulo": titulo,
            "descripcion": "Prueba",
            "precio_noche": 100000,
            "ciudad": "Cali",
        },
        headers=headers,
    )
    return respuesta.get_json()["data"]


def crear_comodidad(client, admin_auth, nombre="WiFi"):
    respuesta = client.post(
        "/api/v1/comodidades",
        json={"nombre": nombre},
        headers=admin_auth,
    )
    return respuesta


def test_admin_crea_comodidad(client, admin_auth):
    respuesta = crear_comodidad(client, admin_auth)

    assert respuesta.status_code == 201
    assert respuesta.get_json()["data"]["nombre"] == "WiFi"


def test_usuario_normal_no_crea_comodidad(client, usuario_auth):
    respuesta = client.post(
        "/api/v1/comodidades",
        json={"nombre": "Piscina"},
        headers=usuario_auth,
    )

    assert respuesta.status_code == 403


def test_comodidad_duplicada_devuelve_409(client, admin_auth):
    crear_comodidad(client, admin_auth, "Parqueadero")
    respuesta = crear_comodidad(client, admin_auth, "Parqueadero")

    assert respuesta.status_code == 409


def test_listar_comodidades_es_publico(client):
    respuesta = client.get("/api/v1/comodidades")

    assert respuesta.status_code == 200
    assert isinstance(respuesta.get_json()["data"], list)


def test_propietario_asigna_comodidad(
    client,
    usuario_auth,
    admin_auth,
):
    alojamiento = crear_alojamiento(client, usuario_auth)
    comodidad = crear_comodidad(
        client,
        admin_auth,
        "Aire acondicionado",
    ).get_json()["data"]

    respuesta = client.patch(
        f"/api/v1/alojamientos/{alojamiento['id']}/comodidades",
        json={"comodidades_ids": [comodidad["id"]]},
        headers=usuario_auth,
    )

    assert respuesta.status_code == 200
    assert respuesta.get_json()["data"]["comodidades"] == [comodidad]


def test_usuario_no_asigna_comodidad_a_alojamiento_ajeno(
    client,
    usuario_auth,
    usuario_auth2,
    admin_auth,
):
    alojamiento = crear_alojamiento(client, usuario_auth, "Casa ajena")
    comodidad = crear_comodidad(
        client,
        admin_auth,
        "Cocina",
    ).get_json()["data"]

    respuesta = client.patch(
        f"/api/v1/alojamientos/{alojamiento['id']}/comodidades",
        json={"comodidades_ids": [comodidad["id"]]},
        headers=usuario_auth2,
    )

    assert respuesta.status_code == 403


def test_asignar_comodidad_inexistente_devuelve_400(
    client,
    usuario_auth,
):
    alojamiento = crear_alojamiento(client, usuario_auth, "Sin comodidad")

    respuesta = client.patch(
        f"/api/v1/alojamientos/{alojamiento['id']}/comodidades",
        json={"comodidades_ids": [999999]},
        headers=usuario_auth,
    )

    assert respuesta.status_code == 400