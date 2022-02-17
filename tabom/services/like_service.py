from typing import cast

from asgiref.sync import sync_to_async
from django.db import transaction
from django.db.models import F

from tabom.models import Article, Like, User


@transaction.atomic
def do_like(user_id: int, article_id: int) -> Like:
    User.objects.filter(id=user_id).get()
    Article.objects.filter(id=article_id).get()

    Article.objects.filter(id=article_id).update(like_count=F("like_count") + 1)
    like = Like.objects.create(user_id=user_id, article_id=article_id)

    # article.save()

    return like


async def async_do_like(user_id: int, article_id: int) -> Like:
    result = await sync_to_async(do_like)(user_id, article_id)
    return cast(Like, result)


@transaction.atomic
def undo_like(user_id: int, article_id: int) -> None:
    # deleted_cnt 는 삭제된 row의 개수
    deleted_cnt, _ = Like.objects.filter(user_id=user_id, article_id=article_id).delete()
    if deleted_cnt:
        Article.objects.filter(id=article_id).update(like_count=F("like_count") - 1)
        # article = Article.objects.filter(id=article_id).get()
        # article.like_count -= 1
        # article.save()


async def async_undo_like(user_id: int, article_id: int) -> None:
    await sync_to_async(undo_like)(user_id, article_id)
