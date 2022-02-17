from django.db import IntegrityError
from django.test import TestCase

from tabom.models import Like
from tabom.models.article import Article
from tabom.models.user import User
from tabom.services.like_service import do_like, undo_like


class TestLikeService(TestCase):
    def test_a_user_can_like_an_article(self) -> None:
        # Given 유저와 게시글이 주어졌을 때
        user = User.objects.create(name="test")
        article = Article.objects.create(title="test_title")

        # When
        like = do_like(user.id, article.id)

        # Then 검증
        self.assertIsNotNone(like.id)
        self.assertEqual(user.id, like.user_id)
        self.assertEqual(article.id, like.article_id)

    # 좋아요는 한개만 가능하다
    def test_a_user_can_like_an_article_only_once(self) -> None:
        # Given
        user = User.objects.create(name="test")
        article = Article.objects.create(title="test_title")

        # Expect
        like1 = do_like(user.id, article.id)
        with self.assertRaises(IntegrityError):
            like2 = do_like(user.id, article.id)

    # user_id가 없는데 Input으로 들어온 경우
    def test_it_should_raise_exception_when_like_an_user_does_not_exist(self) -> None:
        # Given
        invalid_user_id = 9988
        article = Article.objects.create(title="test_title")

        # Expect
        with self.assertRaises(User.DoesNotExist):
            do_like(invalid_user_id, article.id)

    # article_id가 없는데 Input으로 들어온 경우
    def test_it_should_raise_exception_when_like_an_article_does_not_exist(self) -> None:  # 문제
        # Given
        user = User.objects.create(name="test")
        invalid_article_id = 9980

        # Expect
        with self.assertRaises(Article.DoesNotExist):
            do_like(user.id, invalid_article_id)

    # 좋아요 갯수 세기
    def test_like_count_should_increase(self) -> None:  # 됨
        # Given user와 article이 주어짐
        user = User.objects.create(name="test")
        article = Article.objects.create(title="test_title")

        # When  좋아요을 했을 때,
        do_like(user.id, article.id)

        # Then  article을 가져와서 좋아요 갯수를 검증함
        article = Article.objects.get(id=article.id)
        self.assertEqual(1, article.like_count)

    # 좋아요 취소
    def test_a_user_can_undo_like(self) -> None:  # 됨
        # Given
        user = User.objects.create(name="test")
        article = Article.objects.create(title="test_title")
        like = do_like(user.id, article.id)

        # When
        undo_like(user.id, article.id)

        # Then
        with self.assertRaises(Like.DoesNotExist):
            # get을 통해 하나의 모델 object를 가져오려고 할 때, 아무것도 조회되지 않는다면 DoesNotExist 에러 발생
            Like.objects.filter(id=like.id).get()

    # def test_it_should_raise_an_exceotion_when_undo_like_which_does_not_exist(self) -> None:
    #     # Given
    #     user = User.objects.create(name="test")
    #     article = Article.objects.create(title='test_title')
    #
    #     # Expect
    #     with self.assertRaises(Like.DoesNotExist):
    #         undo_like(user.id,article.id)
