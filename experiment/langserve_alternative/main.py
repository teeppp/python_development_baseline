# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Any, Dict, Optional, AsyncGenerator
from sse_starlette.sse import EventSourceResponse
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage, BaseMessageChunk
from uuid import UUID # UUIDをインポート
import json
import uvicorn
import os # 環境変数読み込みのため

# graph.pyからコンパイル済みグラフをインポート
# try...except を一時的に削除してインポートエラーを直接表示させる
from graph import compiled_graph, State
print("Graph imported successfully.")
# except ImportError as e:
#     print(f"Error importing graph: {e}")
#     compiled_graph = None # 仮置き

# --- Pydanticモデル定義 ---
class InvokeRequest(BaseModel):
    """/invoke, /stream_events 共通のリクエストボディ"""
    input: Any # ユーザーからの入力 (例: 文字列)
    config: Optional[Dict[str, Any]] = Field(default_factory=dict)
    # thread_id など、他のLangServeフィールドは最小限のため省略

class InvokeResponse(BaseModel):
    """/invoke のレスポンスボディ"""
    output: Optional[Any] = None # LLMからの最終応答
    metadata: Dict[str, Any] = Field(default_factory=dict) # 実行に関するメタデータ (例: run_id)

# --- FastAPIアプリケーション ---
app = FastAPI(
    title="LangServe Compatible API",
    description="Minimal FastAPI implementation compatible with LangServe invoke/stream_events",
)

# --- ヘルパー関数 ---
def _prepare_run_config(config_dict: Optional[Dict[str, Any]]) -> RunnableConfig:
    """リクエストのconfig辞書からRunnableConfigを作成"""
    return RunnableConfig(configurable=config_dict if config_dict else {})

def _extract_output_from_state(final_state: State) -> Optional[Any]:
    """グラフの最終状態から 'output' に相当するものを抽出"""
    if not final_state or not final_state.get("messages"):
        return None
    # 最後のメッセージがAIからの応答だと仮定
    last_message = final_state["messages"][-1]
    if isinstance(last_message, AIMessage):
        return last_message.content
    return None # 予期しない形式の場合はNone

# --- APIエンドポイント ---

@app.post(
    "/invoke",
    response_model=InvokeResponse,
    summary="Invoke Runnable",
    description="Synchronously invokes the LangGraph runnable.",
)
async def invoke_runnable(request: InvokeRequest):
    """
    グラフを同期的に呼び出し、最終結果を返すエンドポイント。
    LangServeの /invoke と互換性を持たせることを目指す。
    """
    if compiled_graph is None:
        raise HTTPException(status_code=500, detail="Graph not loaded")

    run_config = _prepare_run_config(request.config)
    # グラフへの入力形式をStateに合わせて整形
    input_state = {"messages": [HumanMessage(content=str(request.input))]}

    try:
        # ainvokeを呼び出し (FastAPIは非同期なのでainvokeが適切)
        # 注意: graph.pyのノードも非同期 (async def) であることが望ましい
        final_state: State = await compiled_graph.ainvoke(input_state, config=run_config)

        output = _extract_output_from_state(final_state)

        # メタデータを取得 (ainvokeがrun_idなどを返す場合)
        # 現状のLangGraphのainvokeは直接run_idを返さないことが多い
        # 必要であれば checkpointer を使うか、別の方法でrun_idを取得する必要がある
        metadata = {} # ここでは空

        return InvokeResponse(output=output, metadata=metadata)

    except Exception as e:
        print(f"Error during invoke: {e}")
        # エラーの詳細をログに出力することが望ましい
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


async def event_generator(input_data: Any, config_dict: Optional[Dict[str, Any]]) -> AsyncGenerator[Dict[str, str], None]:
    """
    グラフのastream_eventsを呼び出し、SSE形式でイベントを生成する非同期ジェネレータ。
    """
    if compiled_graph is None:
        # グラフがロードされていない場合のエラーイベント
        yield {
            "event": "error",
            "data": json.dumps({"status_code": 500, "detail": "Graph not loaded"})
        }
        return

    run_config = _prepare_run_config(config_dict)
    input_state = {"messages": [HumanMessage(content=str(input_data))]}

    # --- Helper for safe JSON serialization ---
    def safe_serializer(obj):
        """JSONにシリアライズできないオブジェクトを安全な形式に変換"""
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, BaseMessageChunk):
            # BaseMessageChunkからはcontentなどを抽出 (必要に応じて調整)
            return {"content": obj.content, "type": obj.type}
        # 他のシリアライズ不能な型があればここに追加
        try:
            # それ以外はrepr()で文字列化を試みる
            return repr(obj)
        except Exception:
            return f"<Object of type {type(obj).__name__} is not JSON serializable>"
    # --- End Helper ---

    try:
        # astream_eventsを呼び出し
        async for event in compiled_graph.astream_events(
            input_state,
            config=run_config,
            version="v1" # LangServeで一般的なバージョン
        ):
            # 推測: event["event"] を event名に、辞書全体を data に設定
            # dataはJSON文字列にする必要がある
            try:
                # カスタムシリアライザを使ってJSON文字列に変換
                data_str = json.dumps(event, default=safe_serializer)
            except Exception as serialization_error:
                # シリアライズ中に予期せぬエラーが発生した場合
                print(f"ERROR during event serialization: {serialization_error}")
                print(f"Problematic event data: {event}")
                data_str = json.dumps({
                    "event": event.get("event", "error"),
                    "error": f"Failed to serialize event data: {serialization_error}"
                })

            yield {
                "event": event.get("event", "message"), # イベント名がない場合のデフォルト
                "data": data_str # シリアライズ済みの文字列
            }
    except Exception as e:
         print(f"Error during stream_events: {e}")
         import traceback
         traceback.print_exc()
         # エラーイベントを送信
         yield {
             "event": "error",
             "data": json.dumps({"status_code": 500, "detail": str(e)})
         }

@app.post(
    "/stream_events",
    summary="Stream Events",
    description="Streams events from the LangGraph runnable using Server-Sent Events (SSE).",
)
async def stream_events_runnable(request: InvokeRequest):
     """
     グラフの実行イベントをSSEでストリーミングするエンドポイント。
     LangServeの /stream_events と互換性を持たせることを目指す。
     """
     return EventSourceResponse(event_generator(request.input, request.config))

# --- アプリケーション実行 ---
if __name__ == "__main__":
    # 環境変数からポート番号を取得、なければデフォルト8000
    port = int(os.getenv("PORT", 8000))
    # 環境変数からホストを取得、なければデフォルト0.0.0.0
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run(app, host=host, port=port)

# print("FastAPI app defined.") # 一時的にコメントアウト
# 環境変数 OPENAI_API_KEY のチェック (graph.pyでもチェックしているが念のため)
# if not os.getenv("OPENAI_API_KEY"):
#     print("警告: main.py: OPENAI_API_KEY 環境変数が設定されていません。")
