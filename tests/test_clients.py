import pytest

from app import clients


class _Capture:
    def __init__(self):
        self.calls = []

# --- fetch_topics ---
def test_fetch_topics_calls_expected_url(monkeypatch):
    cap = _Capture()

    def mock_get_json(url):
        cap.calls.append(url)
        return [{"id": "t1", "name": "Topic 1"}]
    
    monkeypatch.setattr(clients, "get_json", mock_get_json)

    response = clients.fetch_topics()
    
    assert response == [{"id": "t1", "name": "Topic 1"}]
    assert len(cap.calls) == 1
    assert cap.calls[0].endswith("/topics")

# --- fetch_skills ---
def test_fetch_skills_calls_expected_url(monkeypatch):
    cap = _Capture()

    def mock_get_json(url):
        cap.calls.append(url)
        return [{"id": "s1", "name": "Skill 1"}]
    
    monkeypatch.setattr(clients, "get_json", mock_get_json)

    response = clients.fetch_skills()
    
    assert response == [{"id": "s1", "name": "Skill 1"}]
    assert len(cap.calls) == 1
    assert cap.calls[0].endswith("/skills")


# --- fetch_resources ---
def test_fetch_resources_with_id(monkeypatch):
    cap = _Capture()

    data = [
        {"id": "r1", "name": "Resource 1"},
        {"_id": 42, "name": "Resource 2"},
        {"_id": "abc", "name": "Resource 3"}
    ]

    def mock_get_json(url):
        cap.calls.append(url)
        return data

    monkeypatch.setattr(clients, "get_json", mock_get_json)

    response = clients.fetch_resources()

    assert len(response) == 3

    assert response[0]["id"] == "r1"
    assert response[1]["id"] == "42"
    assert response[2]["id"] == "abc"

    assert len(cap.calls) == 1
    assert cap.calls[0].endswith("/resources")