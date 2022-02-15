from django.test import TestCase

from tabom.models import Like, User
from tabom.services.article_service import create_an_article
from tabom.services.like_service import do_like


# 현재는 해피패스에 대한 테스트만 작성이 되어 있음
# 해피패스는 API가 성공하는 케이스를 말함
class TestLikeRouter(TestCase):
    def test_post_like(self) -> None:
        # Given
        user = User.objects.create(name="test_user")
        article = create_an_article("test_title")

        # When  // client는 http 흉내를 내어 view 함수 요청을 함
        response = self.client.post(
            "/api/v1/likes/",
            data={
                "user_id": user.id,
                "article_id": article.id,
            },
            content_type="application/json",
        )

        # Then
        self.assertEqual(201, response.status_code)
        # json은 http body를 의미함
        self.assertEqual(user.id, response.json()["user_id"])

    def test_delete_like(self) -> None:
        # Given
        user = User.objects.create(name="test")
        article = create_an_article("test_title")
        like = do_like(user.id, article.id)

        # When //f"/api/v1/likes/?user_id={user.id}&article_id={article.id}" : colistring으로 전달
        response = self.client.delete(f"/api/v1/likes/?user_id={user.id}&article_id={article.id}")

        # Then
        self.assertEqual(204, response.status_code)
        self.assertFalse(Like.objects.filter(id=like.id).exists())
