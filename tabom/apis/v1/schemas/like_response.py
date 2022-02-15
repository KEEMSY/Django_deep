# like model 에서 클라이언트에게 return 해 줄 정보로 "user_id", "article_id", "like_id" (총 3가지)를 내려줌
# updated_at, created_at 은 서버만 가지고 있음
from ninja import Schema


class LikeResponse(Schema):
    # 스키마에 정해져 있지 않은 필드는 클라이언트에게 response로 내려가지 않음
    id: int
    user_id: int
    article_id: int
