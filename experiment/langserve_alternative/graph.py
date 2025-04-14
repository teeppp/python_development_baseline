# graph.py
from typing import Annotated, TypedDict, List
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages, BaseMessage
from langchain_core.prompts import ChatPromptTemplate
# RunnableConfigurableFields の代わりに ConfigurableField をインポート
from langchain_core.runnables.configurable import ConfigurableField
from langchain_openai import ChatOpenAI # 例としてOpenAIを使用
import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む (任意)
load_dotenv()

# 環境変数からAPIキーを設定 (必須)
# OPENAI_API_KEYが設定されていることを確認
if not os.getenv("OPENAI_API_KEY"):
    print("警告: OPENAI_API_KEY 環境変数が設定されていません。")
    # ここでエラーを発生させるか、デフォルトのキーを使うなどの処理を追加できます。
    # raise ValueError("OPENAI_API_KEY must be set")

class State(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    # configurableで受け取る値の例 (オプション)
    # configurable_value: str

def chatbot_node(state: State, config):
    """
    グラフのメインノード。プロンプトを生成し、設定可能なLLMを呼び出す。
    """
    print(f"--- chatbot_node ---")
    print(f"Input State: {state}")
    print(f"Input Config: {config}")

    # stateから最後のメッセージを取得
    # messagesが空でないことを確認
    if not state or not state.get("messages"):
        # 最初の呼び出しなど、メッセージがない場合の処理
        # ここではエラーとするか、デフォルトの応答を返すなどが考えられる
        print("エラー: stateにmessagesが含まれていません。")
        # 例として空の応答を返す
        return {"messages": []}
    last_message = state["messages"][-1].content

    # プロンプトテンプレート
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        ("human", "{input}")
    ])

    # 設定可能なLLMモデル
    # configからモデル名を取得、なければデフォルトを使用
    # configからモデル名を取得する処理は不要になる (ConfigurableFieldで処理される)
    # model_name = config.get("configurable", {}).get("llm_model_name", "gpt-3.5-turbo")
    # print(f"Using LLM model: {model_name}") # configから取得する処理は不要

    # ChatOpenAIの初期化時にデフォルトモデルを指定
    model = ChatOpenAI(model="gpt-3.5-turbo").configurable_fields(
        # ConfigurableField から default 引数を削除
        model_name=ConfigurableField(
            id="llm_model_name",
            name="LLM Model Name",
            description="The OpenAI model to use (e.g., gpt-3.5-turbo, gpt-4)"
            # default="gpt-3.5-turbo" # ここでは指定しない
        )
    )

    # プロンプトとモデルを結合
    chain = prompt | model

    # chainを呼び出し (invokeではなくainvokeを使うのが非同期FastAPIでは一般的だが、
    # ここでは同期的に呼び出す例を示す。必要に応じてainvokeに変更)
    # configを渡して設定可能なフィールドを制御
    try:
        # invokeにconfigを渡す
        response = chain.invoke(
            {"input": last_message},
            config=config # config辞書をそのまま渡す
        )
        print(f"LLM Response: {response}")
        # 応答をStateのmessagesに追加する形式で返す
        return {"messages": [response]}
    except Exception as e:
        print(f"LLM呼び出し中にエラーが発生しました: {e}")
        # エラー発生時の応答を返す (例: エラーメッセージを含むAIMessage)
        from langchain_core.messages import AIMessage
        return {"messages": [AIMessage(content=f"Error during LLM call: {e}")]}


# グラフビルダーの初期化
graph_builder = StateGraph(State)

# ノードを追加
graph_builder.add_node("chatbot", chatbot_node)

# エッジを追加 (開始からchatbotへ、chatbotから終了へ)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# グラフをコンパイル
# checkpointerを追加すると状態管理が可能になるが、今回は最小限のため省略
compiled_graph = graph_builder.compile()

print("Graph compiled successfully.")

# 簡単なテスト用コード (任意)
if __name__ == "__main__":
    from langchain_core.messages import HumanMessage
    # テスト実行
    test_input = {"messages": [HumanMessage(content="Hello!")]}
    test_config = {"configurable": {"llm_model_name": "gpt-3.5-turbo"}}
    try:
        # 同期的に実行
        result = compiled_graph.invoke(test_input, config=test_config)
        print("\n--- Test Result ---")
        print(result)
    except Exception as e:
        print(f"\n--- Test Error ---")
        print(e)

    # ストリームイベントのテスト (非同期)
    import asyncio
    async def stream_test():
        print("\n--- Stream Events Test ---")
        async for event in compiled_graph.astream_events(
            test_input, config=test_config, version="v1"
        ):
            print(event)

    # asyncio.run(stream_test()) # 必要に応じてコメント解除してテスト