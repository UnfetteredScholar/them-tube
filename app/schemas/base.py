from typing import Annotated, Generic, List, Optional, TypeVar

from pydantic import BaseModel, BeforeValidator

PyObjectId = Annotated[Optional[str], BeforeValidator(str)]

T = TypeVar("T")


class Page(BaseModel, Generic[T]):
    items: List[T]
    next_cursor: Optional[str]
