def test_create_bug(client):
    client.post(
        "/requirements/",
        json={
            "id": 400,
            "text": "Для бага",
            "req_type": "functional",
            "device_type": "refrigerator",
        },
    )
    client.post(
        "/testcases/",
        json={
            "id": 500,
            "requirement_id": 400,
            "description": "Тест для бага",
            "steps": ["шаг"],
            "expected_result": "ok",
        },
    )

    response = client.post(
        "/bugs/",
        json={
            "id": 600,
            "title": "Тестовый баг",
            "severity": "medium",
            "steps_to_reproduce": ["шаг1"],
            "actual_result": "ошибка",
            "expected_result": "успех",
            "environment": "тест",
            "test_case_id": 500,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 600


def test_get_bugs(client):
    response = client.get("/bugs/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
