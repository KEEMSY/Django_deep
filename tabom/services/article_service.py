from typing import cast

from asgiref.sync import sync_to_async
from django.db.models import Prefetch, QuerySet

from tabom.models import Article, Like


def create_an_article(title: str) -> Article:
    return Article.objects.create(title=title)


async def async_create_an_article(title: str) -> Article:
    result = await sync_to_async(create_an_article)(title)
    return cast(Article, result)


def get_an_article(user_id: int, article_id: int) -> Article:
    return Article.objects.prefetch_related(
        Prefetch("like_set", queryset=Like.objects.filter(user_id=user_id), to_attr="my_likes")
    ).get(id=article_id)

    # 전 : return Article.objects.filter(id=article_id).get()


async def async_get_an_article(user_id: int, article_id: int) -> Article:
    result = await sync_to_async(get_an_article)(user_id, article_id)
    return cast(Article, result)


def get_article_list(user_id: int, offset: int, limit: int) -> QuerySet[Article]:
    return Article.objects.order_by("-id").prefetch_related(
        Prefetch("like_set", queryset=Like.objects.filter(user_id=user_id), to_attr="my_likes")
    )[offset : offset + limit : 1]


async def async_get_article_list(user_id: int, offset: int, limit: int) -> QuerySet[Article]:
    result = await sync_to_async(get_article_list)(user_id, offset, limit)
    return cast(QuerySet[Article], result)


def delete_an_article(article_id: int) -> None:
    Article.objects.filter(id=article_id).delete()


async def async_delete_an_article(article_id: int) -> None:
    await sync_to_async(delete_an_article)(article_id)


# def get_aricle_list(offset: int, limit: int) -> QuerySet[Article]:
#     # 내림차순 정렬 시 "-", 오름차순은 그냥 빈칸
#     # 쿼리셋도 슬라이싱이 가능함
#     return Article.objects.order_by("-id").prefetch_related("like_set")[offset : offset + limit]


# 공식문서의 pagination을 사용
# def get_article_page(page:int,limit:int)-> Page:
#     return Paginator(Article.objects.order_by("-id"),limit).page(page)
