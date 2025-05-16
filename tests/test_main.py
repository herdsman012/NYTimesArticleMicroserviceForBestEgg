from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_topstories():
    response = client.get("/nytimes/topstories")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 10  # Expecting at least 2 stories from each of 5 categories
    for story in data:
        assert "title" in story
        assert "section" in story
        assert "url" in story
        assert "abstract" in story
        assert "published_date" in story


def test_articlesearch():
    params = {"q": "technology"}
    response = client.get("/nytimes/articlesearch", params=params)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for article in data:
        assert "headline" in article
        assert "snippet" in article
        assert "web_url" in article
        assert "pub_date" in article

def test_articlesearch_missing_query():
    response = client.get("/nytimes/articlesearch")
    assert response.status_code == 422  # Unprocessable Entity due to missing required parameter
