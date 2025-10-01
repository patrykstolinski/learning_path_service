import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(monkeypatch):

    from app import db

    _temp_store = []

    class _SimpleFind(list):
        def sort(self, *args, **kwargs):
            return self
        
    class _MockPaths:
        def insert_one(self, doc):
            data = dict(doc)
            data.setdefault("_id", f"auto-{len(_temp_store) + 1}")
            _temp_store.append(data)
            class Result: ...
            result = Result()
            result.inserted_id = data["_id"]
            return result
        
        def find(self, query=None):
            return _SimpleFind(_temp_store)
        
        def find_one(self, query):
            query = query or {}
            path_id = query.get("pathId") or query.get("_id")
            if path_id is None:
                return _temp_store[0] if _temp_store else None
            
            for item in _temp_store:
                if item.get("pathId") == path_id or item.get("_id") == path_id:
                    return item 

            return None  
        
    monkeypatch.setattr(db, "paths", _MockPaths(), raising=True)
    monkeypatch.setattr(db, "ping", lambda: True, raising=True)


    from app import clients

    def mock_fetch_topics():
        return [
            {"id": "t-react", "name": "React"},
            {"id": "t-testing", "name": "Testing"}
        ]
    
    def mock_fetch_skills():
        return [
            {"id": "s1", "name": "React", "topic_id": "t-react"},
            {"id": "s2", "name": "Testing", "topic_id": "t-testing"}
        ]
    
    def mock_fetch_resources():
        return [
            {"id": "r-1", "title": "Intro to Testing"},
            {"id": "r-2", "title": "React Basics"},
        ]
    
    monkeypatch.setattr(clients, "fetch_topics", mock_fetch_topics)
    monkeypatch.setattr(clients, "fetch_skills", mock_fetch_skills)
    monkeypatch.setattr(clients, "fetch_resources", mock_fetch_resources)


    from app import llm

    def mock_ask_openai_for_plan(desired_skills, desired_topics, topcis, skills, resources):
        return {
            "summary": "Simple demo learning path",
            "milestones": [
                {
                    "milestoneId": "m1",
                    "type": "skill",
                    "label": "Fundamentals",
                    "skillId": "s-basics",
                    "topicId": None,
                    "resources": [{"resourceId": "r-1", "why": "Start here"}],
                    "status": "pending",
                },
                {
                    "milestoneId": "m2",
                    "type": "topic",
                    "label": "Practice React",
                    "skillId": None,
                    "topicId": "t-react",
                    "resources": [{"resourceId": "r-2", "why": "Apply concepts"}],
                    "status": "pending",
                },
            ],
        }
    
    monkeypatch.setattr(llm, "ask_openai_for_plan", mock_ask_openai_for_plan, raising=True)


    from app.main import app

    return TestClient(app)