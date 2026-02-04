def test_chat_stream_endpoint_mock(client):
    payload = {
        "messages": [
            {"role": "user", "content": "Bonjour"}
        ]
    }

    with client.stream("POST", "/chat/stream", json=payload) as response:
        assert response.status_code == 200

        streamed_text = ""
        for chunk in response.iter_text():
            streamed_text += chunk

    assert "[MOCK]" in streamed_text
