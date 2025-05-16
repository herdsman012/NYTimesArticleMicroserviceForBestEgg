from datetime import date
from typing import Dict, List, Optional, Tuple

import httpx
from fastapi import HTTPException, status

from app.config import *


class NYTimesService:
    """
    Service for interacting with the NYT APIs.
    """

    def __init__(self):
        self.api_key = get_settings().nytimes_api_key
        self.top_stories_url = "https://api.nytimes.com/svc/topstories/v2/{section}.json"
        self.article_search_url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"

    async def get_top_stories(self, categories: List[str], stories_per_category: int = 2) -> Tuple[List[Dict], int]:
        all_stories = []

        async with httpx.AsyncClient() as client:
            for category in categories:
                try:
                    params = {"api-key": self.api_key}
                    url = self.top_stories_url.format(section=category)
                    response = await client.get(url, params=params)
                    response.raise_for_status()

                    data = response.json()

                    category_stories = []
                    for story in data.get("results", [])[:stories_per_category]:
                        try:
                            story_data = {
                                "title": story.get("title", ""),
                                "section": story.get("section", ""),
                                "url": story.get("url", ""),
                                "abstract": story.get("abstract", ""),
                                "published_date": story.get("published_date", "")
                            }
                            category_stories.append(story_data)
                        except (KeyError, AttributeError) as e:
                            continue

                    all_stories.extend(category_stories)

                except httpx.HTTPError as exc:
                    error_msg = f"Error fetching top stories for {category}: {str(exc)}"
                    raise HTTPException(
                        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                        detail=error_msg
                    )

        return all_stories, len(all_stories)

    async def search_articles(self,
                              query: str,
                              begin_date: Optional[date] = None,
                              end_date: Optional[date] = None) -> Tuple[List[Dict], int]:

        params = {
            "api-key": self.api_key,
            "q": query,
        }

        # Format dates: YYYYMMDD
        if begin_date:
            params["begin_date"] = begin_date.strftime("%Y%m%d")

        if end_date:
            params["end_date"] = end_date.strftime("%Y%m%d")

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.article_search_url, params=params)
                response.raise_for_status()

                data = response.json()

                articles = []
                for doc in data.get("response", {}).get("docs", []):
                    try:
                        article = {
                            "headline": doc.get("headline", {}).get("main", ""),
                            "snippet": doc.get("snippet", ""),
                            "web_url": doc.get("web_url", ""),
                            "pub_date": doc.get("pub_date", "")
                        }
                        articles.append(article)
                    except (KeyError, AttributeError):
                        continue

                total_hits = data.get("response", {}).get("meta", {}).get("hits", 0)

                return articles, total_hits

        except httpx.HTTPError as exc:
            error_msg = f"Error searching articles: {str(exc)}"
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=error_msg
            )
