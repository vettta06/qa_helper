def test_create_requirement(client):
    response = client.post(
        "/requirements/",
        json={
            "id": 100,
            "text": "Тестовое требование",
            "req_type": "functional",
            "device_type": "refrigerator",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 100
    assert data["text"] == "Тестовое требование"


def test_get_requirements(client):
    response = client.get("/requirements/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1
