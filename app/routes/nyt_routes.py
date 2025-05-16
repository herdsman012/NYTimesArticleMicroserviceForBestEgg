from datetime import date
from typing import Optional

from fastapi import APIRouter, Query, HTTPException, status

from app.models.nyt_model import TopStoriesResponse, ArticleSearchResponse, TopStory, Article
from app.services.nyt_service import NYTimesService

router = APIRouter(prefix="/nytimes", tags=["NYTimes"])

@router.get("/topstories", response_model=TopStoriesResponse, summary="Get top stories")
async def get_top_stories():
    """
    Fetches the two most recent top stories from each of the following categories:
    - arts
    - food
    - movies
    - travel
    - science

    Returns a list of top stories with their details.
    """
    nyt_service = NYTimesService()
    categories = ["arts", "food", "movies", "travel", "science"]

    try:
        stories, total = await nyt_service.get_top_stories(categories)

        story_models = [TopStory(**story) for story in stories]

        return TopStoriesResponse(results=story_models, total=total)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve top stories: {str(e)}"
        )


@router.get("/articlesearch", response_model=ArticleSearchResponse, summary="Search for articles")
async def search_articles(
        q: str = Query(..., description="Search query term"),
        begin_date: Optional[date] = Query(None, description="Begin date (YYYY-MM-DD)"),
        end_date: Optional[date] = Query(None, description="End date (YYYY-MM-DD)")
):
    """
    Searches for articles using the NYTimes Article Search API.

    Parameters:
    - q: Search query term
    - begin_date: Optional start date (YYYY-MM-DD format)
    - end_date: Optional end date (YYYY-MM-DD format)

    Returns articles matching the search criteria.
    """
    nyt_service = NYTimesService()

    try:
        articles, total = await nyt_service.search_articles(q, begin_date, end_date)

        article_models = [Article(**article) for article in articles]

        return ArticleSearchResponse(
            results=article_models,
            total=total,
            query=q
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search articles: {str(e)}"
        )