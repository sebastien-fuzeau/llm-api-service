def test_chat_endpoint_mock(client):
    payload = {
        "messages": [
            {"role": "user", "content": "Bonjour"}
        ]
    }

    response = client.post("/chat", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert "content" in data
    assert data["content"].startswith("[MOCK]")
