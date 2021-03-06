"""
주석 확인
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

"""

from django.test import TestCase

from tabom.models import Like, User
from tabom.models.article import Article
from tabom.services.article_service import (
    create_an_article,
    delete_an_article,
    get_an_article,
    get_article_list,
)
from tabom.services.like_service import do_like


class TestArticleService(TestCase):
    def test_you_can_create_an_article(self) -> None:
        # Given
        title = "test_title"

        # When
        article = create_an_article(title)

        # Then
        self.assertEqual(article.title, title)

    def test_you_can_get_an_article_by_id(self) -> None:
        # Given
        title = "test_title"
        article = create_an_article(title=title)

        # When
        result_article = get_an_article(0, article.id)  # user_id 가 상관없기 때문에 0을 넣은것

        # Then
        self.assertEqual(article.id, result_article.id)
        self.assertEqual(title, result_article.title)

    def test_it_should_raise_exception_when_article_does_not_exist(self) -> None:
        # Given
        invalid_article_id = 9988

        # Expect
        with self.assertRaises(Article.DoesNotExist):
            get_an_article(0, invalid_article_id)

    def test_get_article_list_should_prefetch_like(self) -> None:
        # Given
        user = User.objects.create(name="test_user")
        articles = [create_an_article(title=f"{i}") for i in range(1, 21)]
        do_like(user.id, articles[-1].id)

        # When
        with self.assertNumQueries(2):
            result_articles = get_article_list(user.id, 0, 10)
            result_counts = [a.like_count for a in result_articles]

            # Then
            self.assertEqual(len(result_articles), 10)
            self.assertEqual(1, result_counts[0])
            self.assertEqual(
                [a.id for a in reversed(articles[10:21])],
                [a.id for a in result_articles],
            )

    def test_get_article_list_should_contain_my_likes_when_like_exists(self) -> None:
        # Given
        user = User.objects.create(name="test_user")
        article1 = create_an_article(title="artice1")
        like = do_like(user.id, article1.id)
        create_an_article(title="article2")

        # When
        articles = get_article_list(user.id, 0, 10)

        # Then
        self.assertEqual(like.id, articles[1].my_likes[0].id)
        self.assertEqual(0, len(articles[0].my_likes))

    def test_get_article_list_should_not_contain_my_likes_when_user_id_is_zero(self) -> None:
        # Given
        user = User.objects.create(name="test_user")
        article1 = create_an_article(title="artice1")
        Like.objects.create(user_id=user.id, article_id=article1.id)
        create_an_article(title="article2")
        invalid_user_id = 0

        # When
        articles = get_article_list(invalid_user_id, 0, 10)

        # Then
        self.assertEqual(0, len(articles[1].my_likes))
        self.assertEqual(0, len(articles[0].my_likes))

    def test_you_can_delete_an_article(self) -> None:
        # Given user, article, like를 하나씩 만들고
        user = User.objects.create(name="user1")
        article = create_an_article(title="artice1")
        like = do_like(user.id, article.id)

        # When  article을 삭제했을 때,
        delete_an_article(article.id)

        # Then   article과 like가 삭제되었는지 검증을함
        self.assertFalse(Article.objects.filter(id=article.id).exists())
        self.assertFalse(Like.objects.filter(id=like.id).exists())
