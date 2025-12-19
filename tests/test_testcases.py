def test_create_testcase(client):
    client.post(
        "/requirements/",
        json={
            "id": 200,
            "text": "Для тест-кейса",
            "req_type": "functional",
            "device_type": "refrigerator",
        },
    )

    response = client.post(
        "/testcases/",
        json={
            "id": 300,
            "requirement_id": 200,
            "description": "Тестовый кейс",
            "steps": ["шаг1", "шаг2"],
            "expected_result": "успех",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 300


def test_get_testcases(client):
    response = client.get("/testcases/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
