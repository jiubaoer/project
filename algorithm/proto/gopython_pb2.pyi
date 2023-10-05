from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DisReply(_message.Message):
    __slots__ = ["dis"]
    DIS_FIELD_NUMBER: _ClassVar[int]
    dis: int
    def __init__(self, dis: _Optional[int] = ...) -> None: ...

class DisRequest(_message.Message):
    __slots__ = ["path"]
    PATH_FIELD_NUMBER: _ClassVar[int]
    path: str
    def __init__(self, path: _Optional[str] = ...) -> None: ...
