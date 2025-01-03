import mesop as me
from data_model import State, APIPath, ModelDialogState, Conversation, ChatMessage
from dialog import dialog, dialog_actions
from api_client import ChatMessage
import api_client

def change_api_path(e: me.RadioChangeEvent):
    s = me.state(ModelDialogState)
    s.selected_api_path = e.value

def api_path_dialog():
    state = me.state(State)
    with dialog(state.is_model_picker_dialog_open):
        me.text("APIパスを選択")
        with me.box(style=me.Style(display="flex", flex_direction="column", gap=12, padding=me.Padding(top=12))):
                # for api_path in APIPath:
            me.button_toggle(
                # label=api_path.display_name,
                value=state.selected_api_path,
                buttons=[me.ButtonToggleButton(label=api_path.display_name, value=api_path.value) for api_path in APIPath],
                on_change=change_api_path,
                # style=me.Style(
                #     display="flex",
                #     flex_direction="column",
                #     gap=4,
                # ),
            )
        with dialog_actions():
            me.button("キャンセル", on_click=close_api_path_dialog)
            me.button("確定", on_click=confirm_api_path_dialog)
def close_api_path_dialog(e: me.ClickEvent):
    state = me.state(State)
    state.is_model_picker_dialog_open = False

def confirm_api_path_dialog(e: me.ClickEvent):
    dialog_state = me.state(ModelDialogState)
    state = me.state(State)
    state.is_model_picker_dialog_open = False
    state.selected_api_path = dialog_state.selected_api_path

ROOT_BOX_STYLE = me.Style(
    background="#e7f2ff",
    height="100%",
    font_family="Inter",
    display="flex",
    flex_direction="column",
)
STYLESHEETS = [
  "https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap"
]

@me.page(
    path="/",
    stylesheets=STYLESHEETS,
    security_policy=me.SecurityPolicy(
        dangerously_disable_trusted_types=True
    )
)
def home_page():
    api_path_dialog()
    with me.box(style=ROOT_BOX_STYLE):
        header()
        with me.box(
            style=me.Style(
                width="min(680px, 100%)",
                margin=me.Margin.symmetric(horizontal="auto", vertical=36),
            )
        ):
            me.text(
                "Chat with API",
                style=me.Style(font_size=20, margin=me.Margin(bottom=24)),
            )
            mode_switch()
            examples_row()
            chat_input()

EXAMPLES = [
    "AIエージェントフレームワークの最新情報を教えて",
    "Pythonの次に覚えやすいフロントエンド向けプログラミング言語は？",
    "革新的な最新技術について",
]

def examples_row():
    with me.box(
        style=me.Style(
            display="flex", flex_direction="row", gap=16, margin=me.Margin(bottom=24)
        )
    ):
        for i in EXAMPLES:
            example(i)

def example(text: str):
    with me.box(
        key=text,
        on_click=click_example,
        style=me.Style(
            cursor="pointer",
            background="#b9e1ff",
            width="215px",
            height=160,
            font_weight=500,
            line_height="1.5",
            padding=me.Padding.all(16),
            border_radius=16,
            border=me.Border.all(me.BorderSide(width=1, color="blue", style="none")),
        ),
    ):
        me.text(text)

def click_example(e: me.ClickEvent):
    state = me.state(State)
    state.input = e.key

@me.page(path="/conversation", stylesheets=STYLESHEETS)
def conversation_page():
    state = me.state(State)
    api_path_dialog()
    with me.box(style=ROOT_BOX_STYLE):
        header()

        models = len(state.conversations)
        models_px = models * 680
        with me.box(
            style=me.Style(
                width=f"min({models_px}px, calc(100% - 32px))",
                display="grid",
                gap=16,
                grid_template_columns=f"repeat({models}, 1fr)",
                flex_grow=1,
                overflow_y="hidden",
                margin=me.Margin.symmetric(horizontal="auto"),
                padding=me.Padding.symmetric(horizontal=16),
            )
        ):
            for conversation in state.conversations:
                api_path = conversation.api_path
                messages = conversation.messages
                with me.box(
                    style=me.Style(
                        overflow_y="auto",
                    )
                ):
                    me.text("API Path: " + api_path, style=me.Style(font_weight=500))

                    for message in messages:
                        # print(message)
                        if message.role == "user":
                            user_message(message.content)
                        else:
                            model_message(message)
                    if messages and api_path == state.conversations[-1].api_path:
                        me.box(
                            key="end_of_messages",
                            style=me.Style(
                                margin=me.Margin(
                                    bottom="50vh" if messages[-1].in_progress else 0
                                )
                            ),
                        )
        with me.box(
            style=me.Style(
                display="flex",
                justify_content="center",
            )
        ):
            with me.box(
                style=me.Style(
                    width="min(680px, 100%)",
                    padding=me.Padding(top=24, bottom=24),
                )
            ):
                chat_input()

def user_message(content: str):
    with me.box(
        style=me.Style(
            background="#e7f2ff",
            padding=me.Padding.all(16),
            margin=me.Margin.symmetric(vertical=16),
            border_radius=16,
        )
    ):
        me.text(content)

def model_message(message: ChatMessage):
    with me.box(
        style=me.Style(
            background="#fff",
            padding=me.Padding.all(16),
            border_radius=16,
            margin=me.Margin.symmetric(vertical=16),
        )
    ):
        me.markdown(message.content)
        if message.in_progress:
            me.progress_spinner()

def header():
    with me.box(
        style=me.Style(
            padding=me.Padding.all(16),
        ),
    ):
        me.text(
            "API Chat",
            style=me.Style(
                font_weight=500,
                font_size=24,
                color="#3D3929",
                letter_spacing="0.3px",
            ),
        )

def switch_api_path(e: me.ClickEvent):
    state = me.state(State)
    state.is_model_picker_dialog_open = True
    dialog_state = me.state(ModelDialogState)
    dialog_state.selected_api_path = state.selected_api_path

def mode_switch():
    state = me.state(State)
    with me.box(style=me.Style(flex_grow=1)):
        with me.box(
            style=me.Style(
                display="flex",
                padding=me.Padding(left=12, bottom=12),
                cursor="pointer",
            ),
            on_click=switch_api_path,
        ):
            me.text(
                "API Path:",
                style=me.Style(font_weight=500, padding=me.Padding(right=6)),
            )
            me.text(APIPath(state.selected_api_path).display_name)
def chat_input():
    state = me.state(State)
    with me.box(
        style=me.Style(
            border_radius=16,
            padding=me.Padding.all(8),
            background="white",
            display="flex",
            width="100%",
        )
    ):
        with me.box(style=me.Style(flex_grow=1)):
            me.native_textarea(
                value=state.input,
                placeholder="メッセージを入力",
                on_blur=on_blur,
                style=me.Style(
                    padding=me.Padding(top=16, left=16),
                    outline="none",
                    width="100%",
                    border=me.Border.all(me.BorderSide(style="none")),
                ),
            )
        with me.content_button(
            type="icon", on_click=send_prompt
        ):
            me.icon("send")

def on_blur(e: me.InputBlurEvent):
    state = me.state(State)
    state.input = e.value

def send_prompt(e: me.ClickEvent):
    state = me.state(State)
    if not state.conversations:
        me.navigate("/conversation")
        state.conversations.append(Conversation(api_path=state.selected_api_path, messages=[]))
    input = state.input
    state.input = ""
    # print(input)

    for conversation in state.conversations:
        api_path = conversation.api_path
        messages = conversation.messages
        messages.append(ChatMessage(role="user", content=input))
        messages.append(ChatMessage(role="model", content="", in_progress=True))
        yield
        me.scroll_into_view(key="end_of_messages")
        
        try:
            if api_path == APIPath.INVOKE.value:
                messages[-1].content = api_client.send_normal_message(input)
            else:
                api_func = (api_client.send_stream_message
                          if api_path == APIPath.STREAM.value
                          else api_client.send_stream_messages)
                
                for chunk in api_func(input):
                    messages[-1].content += chunk
                    # print(chunk)
                    yield
        except Exception as e:
            messages[-1].content = f"Error: {str(e)}"
        messages[-1].in_progress = False
        yield
