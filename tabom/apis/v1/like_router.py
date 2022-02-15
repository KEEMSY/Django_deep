from typing import Tuple

from django.http import HttpRequest
from ninja import Router

from tabom.apis.v1.schemas.like_response import LikeResponse
from tabom.apis.v1.schemas.like_schema import LikeRequest
from tabom.models import Like
from tabom.services.like_service import undo_like, do_like

router = Router()


@router.post("/", response={201: LikeResponse})  # like_request: LikeRequest -> 스키마 사용
def post_like(request: HttpRequest, like_request: LikeRequest) -> Tuple[int, Like]:
    like = do_like(user_id=like_request.user_id, article_id=like_request.article_id)
    # 만들어졌다고 알려주는 status code 는 201번 // 파이썬 문법상, 2개이상을 리턴하면 tuple로 묶음
    return 201, like


# router의 데코레이터의 response를 명시를 해야 swagger에서 제대로 생성이 됨
# // 만들 때에는 status code를 적고, 어떤 response를 사용할지 적어주면 됨
@router.delete("/", response={204: LikeResponse})
# delete에서는 body를 안쓰는 것이 표준(좀 더 안전한 방법)
def delete_like(request: HttpRequest, user_id: int, article_id: int) -> Tuple[int, None]:
    undo_like(user_id=user_id, article_id=article_id)
    # 204는 "response body가 없다 = no contents" 를 의미함 -> 삭제가 되면, 삭제가 성공했다는 것만 알려주면 됨
    return 204, None
