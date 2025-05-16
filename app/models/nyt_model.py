from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional
from datetime import date


class TopStory(BaseModel):
    title: str
    section: str
    url: HttpUrl
    abstract: str
    published_date: str


class TopStoriesResponse(BaseModel):
    results: List[TopStory]
    total: int = Field(..., )


class Article(BaseModel):
    headline: str
    snippet: str
    web_url: HttpUrl
    pub_date: str


class ArticleSearchParams(BaseModel):
    q: str = Field(..., )
    begin_date: Optional[date] = Field(None, )
    end_date: Optional[date] = Field(None, )


class ArticleSearchResponse(BaseModel):
    results: List[Article]
    total: int = Field(..., )
    query: str = Field(..., )
