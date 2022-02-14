# from datetime import datetime
# from time import sleep
#
# from django.db import connection
# from django.test import TestCase
#
# from tabom.models import User
#
#
# # updated_at 과 created_at에 아무값도 입력하지 않고 값이 입력되있는지 확인하는 것
# # 장고의 테스트는 별도의 데이터베이스에서 이루어짐
# class TestAutoNow(TestCase):
#     # 함수이름은 test_로 시작해야함("TestCase"가 test인것을 찾아서 실행해줌)
#     def test_auto_now_field_is_set_when_save(self) -> None:  # 테스트케이스는 리턴하는것이 없어야함
#         user = User(name='test')
#         user.save()
#         self.assertIsNone(user.updated_at)
#         self.assertIsNone(user.created_at)
#
#     def test_auto_now_field_not_set_when_raw_sql_update_executed(self) -> None:
#         # Given
#         with connection.cursor() as cursor:
#             cursor.execute(
#                 "INSERT INTO tabom_user(id, name, updated_at, created_at) "
#                 "VALUES (1, 'hihi', '1999-01-01 10:10:10', '1999-01-01 10:10:10')"
#             )
#
#             # When
#             sleep(1)
#             cursor.execute(
#                 "UPDATE tabom_user SET name='changed' WHERE id=1"
#             )
#
#         # Then
#         user = User.objects.filter(id=1).get()
#         self.assertEqual(user.updated_at, datetime(year=1999, month=1, day=1, hour=10, minute=10, second=10))
