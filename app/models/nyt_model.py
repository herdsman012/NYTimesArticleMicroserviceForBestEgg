from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional
from datetime import date


class TopStory(BaseModel):
    """
    Model representing a top story from NYT Top Stories API.
    """
    title: str
    section: str
    url: HttpUrl
    abstract: str
    published_date: str


class TopStoriesResponse(BaseModel):
    """
    Response model for the top stories endpoint.
    """
    results: List[TopStory]
    total: int = Field(..., description="Total number of stories returned")


class Article(BaseModel):
    """
    Model representing an article from NYT Article Search API.
    """
    headline: str
    snippet: str
    web_url: HttpUrl
    pub_date: str


class ArticleSearchParams(BaseModel):
    """
    Request parameters for article search.
    """
    q: str = Field(..., description="Search query term")
    begin_date: Optional[date] = Field(None, description="Begin date (YYYY-MM-DD)")
    end_date: Optional[date] = Field(None, description="End date (YYYY-MM-DD)")


class ArticleSearchResponse(BaseModel):
    """
    Response model for the article search endpoint.
    """
    results: List[Article]
    total: int = Field(..., description="Total number of articles found")
    query: str = Field(..., description="The search query that was used")
