def test_read_vehicles_empty(client):
    """Debe retornar lista vacía si no hay autos"""
    response = client.get("/api/v1/vehicles/")
    assert response.status_code == 200
    assert response.json() == []


def test_read_vehicles_with_data(client, create_test_vehicle):
    """Debe retornar el auto creado por la fixture"""
    response = client.get("/api/v1/vehicles/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["brand"] == "TestBrand"
    assert data[0]["model"] == "TestModel"
