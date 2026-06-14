from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class Result(BaseModel, Generic[T]):
    """统一返回体"""
    code: int = 200
    message: str = "success"
    data: T | None = None

    @classmethod
    def ok(cls, data: T | None = None, message: str = "success") -> "Result[T]":
        """成功响应"""
        return cls(code=200, message=message, data=data)

    @classmethod
    def fail(
        cls,
        code: int = 400,
        message: str = "error",
        data: T | None = None,
    ) -> "Result[T]":
        """失败响应"""
        return cls(code=code, message=message, data=data)
