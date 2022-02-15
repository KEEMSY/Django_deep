from tabom.models import Article, Like, User


def do_like(user_id: int, article_id: int) -> Like:
    User.objects.filter(id=user_id).get()
    Article.objects.filter(id=article_id).get()

    return Like.objects.create(user_id=user_id, article_id=article_id)


def undo_like(user_id: int, article_id: int) -> None:
    Like.objects.filter(user_id=user_id, article_id=article_id).delete()
