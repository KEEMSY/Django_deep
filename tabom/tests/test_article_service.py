from django.test import TestCase

from tabom.models import User
from tabom.models.article import Article
from tabom.services.article_service import get_an_article, get_article_list
from tabom.services.like_service import do_like


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

    def test_get_article_list_should_prefetch_like(self) -> None:
        # Given
        user = User.objects.create(name="test_user")
        articles = [Article.objects.create(title=f"{i}") for i in range(1, 21)]
        do_like(user.id, articles[-1].id)

        # When
        # with CaptureQueriesContext(connection) as ctx:
        with self.assertNumQueries(3):  # 몇번의 쿼리가 발생할지 테스트를 함 article 조회 1번, Like count 1번 총 2번의 쿼리 발생
            result_article = get_article_list(user.id, 0, 10)
            result_counts = [a.like_set.count() for a in result_article]

            # Then
            self.assertEqual(len(result_article), 10)
            self.assertEqual(1, result_counts[0])
            self.assertEqual(
                [a.id for a in reversed(articles[10:21])],  # reversed가 되었기 때문에 내림차순 정렬이 됨
                [a.id for a in result_article],
            )

    # 클래스를 이용한 pagination임
    # def test_get_article_page_should_prefetch_like(self) -> None:
    #     # Given
    #     user = User.objects.create(name='test_user')
    #     articles =[Article.objects.create(title=f"{i}") for i in range(1,21)]
    #     do_like(user.id, articles[-1].id)
    #
    #     # When
    #     result_article = get_article_page(1,10)
    #
    #     # Then
    #     self.assertEqual(len(result_article),10)
    #     self.assertEqual(1,result_article[0].like_set.count())
    #     self.assertEqual(
    #         [a.id for a in reversed(articles[10:21])],   #reversed가 되었기 때문에 내림차순 정렬이 됨
    #         [a.id for a in result_article],
    #     )

    def test_get_article_list_should_contain_my_like_when_like_exists(self) -> None:
        # Given
        user = User.objects.create(name="test_user")
        article1 = Article.objects.create(title="artice1")
        like = do_like(user.id, article1.id)
        Article.objects.create(title="article2")

        # When
        articles = get_article_list(user.id, 0, 10)  # user_id를 받는 이유는 어떤 유저가 요청을 했는지 알기위함

        # Then
        self.assertEqual(like.id, articles[1].my_likes[0].id)
        self.assertEqual(0, len(articles[0].my_likes))
