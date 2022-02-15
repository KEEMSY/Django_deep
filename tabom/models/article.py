from typing import Any, List

from django.db import models

from tabom.models.base_model import BaseModel


class Article(BaseModel):
    title = models.CharField(max_length=255)
    my_likes: List[Any]   # mypy가 인식할 수 있도록 만들어둔 것
