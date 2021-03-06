"""
from typing import List, Tuple

from django.db.models import QuerySet
from django.http import HttpRequest
from ninja import Router
from ninja.errors import HttpError

from tabom.apis.v1.schemas.article_create_request import ArticleCreateRequest
from tabom.apis.v1.schemas.article_response import ArticleResponse
from tabom.models import Article
from tabom.services.article_service import (
    create_an_article,
    delete_an_article,
    get_an_article,
    get_article_list,
)

router = Router(tags=["articles"])


# article 생성에 관한 코드 // 생성이 완료되었다고 알려주는 status code는 201
@router.post("/", response={201: ArticleResponse})
def create_article(request: HttpRequest, article_create_request: ArticleCreateRequest) -> Tuple[int, Article]:
    article = create_an_article(article_create_request.title)
    return 201, article


# 기본적을 성공을 할 때에는 200의 status code가 가기 때문에 200일 쓸 때에는 딱히 명시 하지않고
# 스키마만 사용할 수 있음.
# 리스트 조회 : 리스트를 감싼 schema를 return
@router.get("/", response=List[ArticleResponse])
def get_articles(request: HttpRequest, user_id: int, offset: int = 0, limit: int = 10) -> QuerySet[Article]:
    articles = get_article_list(user_id, offset, limit)
    return articles


# 단건 조회 : 그냥 schemafmf return
@router.get("/{article_id}", response=ArticleResponse)
def get_article(request: HttpRequest, user_id: int, article_id: int) -> Article:
    try:
        aritlcle = get_an_article(user_id, article_id)
    except Article.DoesNotExist:
        raise HttpError(404, f"Article #{article_id} Not Found")
    return aritlcle


@router.delete("/{article_id}", response={204: None})
def delete_article(request: HttpRequest, article_id: int) -> Tuple[int, None]:
    delete_an_article(article_id)
    return 204, None
"""

from typing import List, Tuple

from django.db.models import QuerySet
from django.http import HttpRequest
from ninja import Router
from ninja.errors import HttpError

from tabom.apis.v1.schemas.article_create_request import ArticleCreateRequest
from tabom.apis.v1.schemas.article_response import ArticleResponse
from tabom.models import Article
from tabom.services.article_service import (
    async_create_an_article,
    async_delete_an_article,
    async_get_an_article,
    async_get_article_list,
)

router = Router(tags=["articles"])


@router.post("/", response={201: ArticleResponse})
async def create_article(request: HttpRequest, article_create_request: ArticleCreateRequest) -> Tuple[int, Article]:
    article = await async_create_an_article(article_create_request.title)
    return 201, article


@router.get("/", response=List[ArticleResponse])
async def get_articles(request: HttpRequest, user_id: int, offset: int = 0, limit: int = 10) -> QuerySet[Article]:
    articles = await async_get_article_list(user_id, offset, limit)
    return articles


@router.get("/{article_id}", response=ArticleResponse)
async def get_article(request: HttpRequest, user_id: int, article_id: int) -> Article:
    try:
        aritlcle = await async_get_an_article(user_id, article_id)
    except Article.DoesNotExist:
        raise HttpError(404, f"Article #{article_id} Not Found")
    return aritlcle


@router.delete("/{article_id}", response={204: None})
async def delete_article(request: HttpRequest, article_id: int) -> Tuple[int, None]:
    await async_delete_an_article(article_id)
    return 204, None
