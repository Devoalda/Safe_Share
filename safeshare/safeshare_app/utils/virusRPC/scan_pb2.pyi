from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ScanFileRequest(_message.Message):
    __slots__ = ["file_name", "file_SHA256", "file_SHA1", "file_MD5"]
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    FILE_SHA256_FIELD_NUMBER: _ClassVar[int]
    FILE_SHA1_FIELD_NUMBER: _ClassVar[int]
    FILE_MD5_FIELD_NUMBER: _ClassVar[int]
    file_name: str
    file_SHA256: str
    file_SHA1: str
    file_MD5: str
    def __init__(self, file_name: _Optional[str] = ..., file_SHA256: _Optional[str] = ..., file_SHA1: _Optional[str] = ..., file_MD5: _Optional[str] = ...) -> None: ...

class ScanFileResponse(_message.Message):
    __slots__ = ["file_name", "file_SHA256", "file_SHA1", "file_MD5", "is_infected", "scan_result", "scan_result_detail"]
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    FILE_SHA256_FIELD_NUMBER: _ClassVar[int]
    FILE_SHA1_FIELD_NUMBER: _ClassVar[int]
    FILE_MD5_FIELD_NUMBER: _ClassVar[int]
    IS_INFECTED_FIELD_NUMBER: _ClassVar[int]
    SCAN_RESULT_FIELD_NUMBER: _ClassVar[int]
    SCAN_RESULT_DETAIL_FIELD_NUMBER: _ClassVar[int]
    file_name: str
    file_SHA256: str
    file_SHA1: str
    file_MD5: str
    is_infected: bool
    scan_result: str
    scan_result_detail: str
    def __init__(self, file_name: _Optional[str] = ..., file_SHA256: _Optional[str] = ..., file_SHA1: _Optional[str] = ..., file_MD5: _Optional[str] = ..., is_infected: bool = ..., scan_result: _Optional[str] = ..., scan_result_detail: _Optional[str] = ...) -> None: ...
