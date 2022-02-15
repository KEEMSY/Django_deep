from typing import List, Optional

from ninja import Schema

from tabom.apis.v1.schemas.like_response import LikeResponse


class ArticleResponse(Schema):
    id: int
    title: str
    # Optional : 이 값이 List[LikeResponse] 일 수 도 있고, 아니면 None 일 수 도 있다.//  non 이거나 존재하거나 할 수 있다.
    # None 일수도 있는 값을 지정하고 싶을 때, Optional을 사용함
    my_likes: Optional[List[LikeResponse]]
