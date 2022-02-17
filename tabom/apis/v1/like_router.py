"""
from typing import Tuple

from django.db import IntegrityError
from django.http import HttpRequest
from ninja import Router
from ninja.errors import HttpError

from tabom.apis.v1.schemas.like_response import LikeResponse
from tabom.apis.v1.schemas.like_schema import LikeRequest
from tabom.models import Article, Like, User
from tabom.services.like_service import do_like, undo_like

router = Router(tags=["likes"])


@router.post("/", response={201: LikeResponse})  # like_request: LikeRequest -> 스키마 사용
def post_like(request: HttpRequest, like_request: LikeRequest) -> Tuple[int, Like]:
    try:
        like = do_like(user_id=like_request.user_id, article_id=like_request.article_id)
    # 만들어졌다고 알려주는 status code 는 201번 // 파이썬 문법상, 2개이상을 리턴하면 tuple로 묶음
    except User.DoesNotExist:
        raise HttpError(404, f"User #{like_request.user_id} Not Found")
    except Article.DoesNotExist:
        raise HttpError(404, f"Article #{like_request.article_id} Not Found")
    except IntegrityError:  # IntegritityError의 경우 like가 중복될 때 밖에 없음
        raise HttpError(400, "duplicate like")
    return 201, like


# router의 데코레이터의 response를 명시를 해야 swagger에서 제대로 생성이 됨
# // 만들 때에는 status code를 적고, 어떤 response를 사용할지 적어주면 됨
@router.delete("/", response={204: None})
# delete에서는 body를 안쓰는 것이 표준(좀 더 안전한 방법)
def delete_like(request: HttpRequest, user_id: int, article_id: int) -> Tuple[int, None]:
    undo_like(user_id=user_id, article_id=article_id)
    # 204는 "response body가 없다 = no contents" 를 의미함 -> 삭제가 되면, 삭제가 성공했다는 것만 알려주면 됨
    return 204, None
"""


from typing import Tuple

from django.db import IntegrityError
from django.http import HttpRequest
from ninja import Router
from ninja.errors import HttpError

from tabom.apis.v1.schemas.like_response import LikeResponse
from tabom.apis.v1.schemas.like_schema import LikeRequest
from tabom.models import Article, Like, User
from tabom.services.like_service import async_do_like, async_undo_like

router = Router(tags=["likes"])


@router.post("/", response={201: LikeResponse})
async def post_like(request: HttpRequest, like_request: LikeRequest) -> Tuple[int, Like]:
    try:
        like = await async_do_like(user_id=like_request.user_id, article_id=like_request.article_id)
    except User.DoesNotExist:
        raise HttpError(404, f"User #{like_request.user_id} Not Found")
    except Article.DoesNotExist:
        raise HttpError(404, f"Article #{like_request.article_id} Not Found")
    except IntegrityError:
        raise HttpError(400, "duplicate like")
    return 201, like


@router.delete("/", response={204: None})
async def delete_like(request: HttpRequest, user_id: int, article_id: int) -> Tuple[int, None]:
    await async_undo_like(user_id=user_id, article_id=article_id)
    return 204, None
