from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Request(_message.Message):
    __slots__ = ["file_hash"]
    FILE_HASH_FIELD_NUMBER: _ClassVar[int]
    file_hash: str
    def __init__(self, file_hash: _Optional[str] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ["is_exist"]
    IS_EXIST_FIELD_NUMBER: _ClassVar[int]
    is_exist: bool
    def __init__(self, is_exist: bool = ...) -> None: ...
