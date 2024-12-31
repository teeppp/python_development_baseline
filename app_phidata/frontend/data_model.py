from dataclasses import dataclass, field
from typing import Literal
from enum import Enum

import mesop as me

Role = Literal["user", "model"]

@dataclass(kw_only=True)
class ChatMessage:
    role: Role = "user"
    content: str = ""
    in_progress: bool = False

class APIPath(Enum):
    INVOKE = "/invoke"
    STREAM = "/stream"
    STREAM_MESSAGES = "/stream-messages"

    @property
    def display_name(self) -> str:
        return {
            self.INVOKE: "通常レスポンス",
            self.STREAM: "ストリーム",
            self.STREAM_MESSAGES: "メッセージストリーム"
        }[self]

@dataclass
class Conversation:
    api_path: str = ""
    messages: list[ChatMessage] = field(default_factory=list)

@me.stateclass
class State:
    is_model_picker_dialog_open: bool = False
    input: str = ""
    conversations: list[Conversation] = field(default_factory=list)
    selected_api_path: str = APIPath.INVOKE.value

@me.stateclass
class ModelDialogState:
    selected_api_path: str = APIPath.INVOKE.value