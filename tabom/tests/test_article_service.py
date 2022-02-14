from django.test import TestCase

from tabom.models.article import Article
from tabom.services.article_service import get_an_article


class TestArticleService(TestCase):
    # article_id로 게시물을 조회할 수 있다.
    def test_you_can_get_an_article_by_id(self) -> None:
        # Given
        title = "test_title"
        article = Article.objects.create(title=title)

        # When
        result_article = get_an_article(article.id)

        # Then 조회한 article_id와 result로 나온 article_id 가 같은지 비교
        self.assertEqual(article.id, result_article.id)
        self.assertEqual(title, result_article.title)

    def test_it_should_raise_exception_when_article_does_not_exist(self) -> None:
        # Given 없는 article_id를 제시
        invalid_article_id = 9988

        # Expect
        with self.assertRaises(Article.DoesNotExist):
            get_an_article(invalid_article_id)
