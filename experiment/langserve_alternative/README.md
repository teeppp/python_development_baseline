# LangServe代替 FastAPI実装

このプロジェクトは、LangServeの主要機能、特に `/invoke` および `/stream_events` エンドポイントと `configurable` パラメータのサポートに互換性を持つように設計された、最小限のFastAPI実装を提供します。LangGraphアプリケーションをAPIとしてデプロイするための、完全にオープンソースな代替手段として機能します。

## 機能

*   **LangServe互換性 (最小限):** LangServeと同様の `/invoke` および `/stream_events` エンドポイントを実装。
*   **Configurableサポート:** リクエストボディの `config` フィールドを介して設定（例: LLMモデル名）を渡し、それをLangGraphランナブルに適用可能。
*   **SSEストリーミング:** `/stream_events` エンドポイントでServer-Sent Events (SSE) を使用し、実行イベントをリアルタイムでストリーミング。
*   **オープンソース:** FastAPI、LangChain、LangGraphなど、完全にオープンソースのライブラリで構築。
*   **シンプルなグラフ例:** OpenAIを使用した設定可能なチャットボットノードを示す基本的なLangGraph定義 (`graph.py`) を含む。

## ファイル構成

```
.
├── graph.py       # LangGraphグラフのロジックを定義
├── main.py        # /invoke, /stream_events エンドポイントを持つFastAPIアプリケーション
├── sse_client.py  # /stream_events エンドポイントをテストするためのPythonスクリプト
└── README.md      # このファイル
└── .env           # (任意) APIキーなどの環境変数を格納
```

## 必要なライブラリ

*   Python 3.13
*   以下のライブラリ (`uv` でインストール):
    *   `fastapi`
    *   `uvicorn`
    *   `langchain`
    *   `langgraph`
    *   `sse-starlette`
    *   `pydantic`
    *   `langchain-openai` (`graph.py` で使用する他のLLMプロバイダーライブラリでも可)
    *   `python-dotenv` (`.env` ファイル読み込み用、任意)
    *   `httpx` (`sse_client.py` 実行用)

以下のコマンドでインストールできます:
```bash

uv add fastapi uvicorn langchain langgraph sse-starlette pydantic langchain-openai python-dotenv httpx
```

## セットアップ

1.  **環境変数:** この例ではOpenAI APIを使用します。`OPENAI_API_KEY` 環境変数を設定する必要があります。以下のいずれかの方法で設定してください:
    *   プロジェクトルートディレクトリに `.env` ファイルを作成し、`OPENAI_API_KEY=sk-your_openai_api_key` のように記述します（実際のキーに置き換えてください）。
    *   ターミナルで変数をエクスポートします: `export OPENAI_API_KEY=sk-your_openai_api_key`

## サーバーの実行

ターミナルでプロジェクトディレクトリ (`experiment/langserve_alternative`) に移動し、Uvicornを使用してFastAPIサーバーを実行します:

```bash
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

*   `--host 0.0.0.0`: サーバーを外部からアクセス可能にします（ローカルアクセスのみの場合は `127.0.0.1` を使用）。
*   `--port 8000`: ポート番号を指定します。
*   `--reload`: コード変更時にサーバーを自動的にリロードします（開発時に便利）。

サーバーは `http://0.0.0.0:8000` で起動します。

## APIのテスト

### 1. `/invoke` のテスト

別のターミナルで `curl` を使用してPOSTリクエストを送信します:

```bash
curl -X POST http://127.0.0.1:8000/invoke \
     -H "Content-Type: application/json" \
     -d '{"input": "LangGraphとは何ですか？", "config": {"llm_model_name": "gpt-3.5-turbo"}}'
```

*   `"LangGraphとは何ですか？"` を任意の入力に置き換えてください。
*   `"config"` ディクショナリを変更して、異なる設定（例: `"llm_model_name"` を `"gpt-4"` に変更）を渡すことができます。

以下のようなJSONレスポンスが返されるはずです:
```json
{"output": "LangGraphは、LLMを使用してステートフルでマルチアクターなアプリケーションを構築するためのライブラリです...", "metadata": {}}
```

### 2. `/stream_events` のテスト

提供されているPythonスクリプト `sse_client.py` を使用します:

```bash
uv run python sse_client.py
```

このスクリプトは `/stream_events` エンドポイントに接続し、受信したServer-Sent Eventsを以下の形式で表示します:

```
event: <イベント名>
data: <JSONペイロード>
```

`on_chain_start`, `on_prompt_start`, `on_chat_model_start`, `on_chat_model_stream` (コンテンツのチャンクを含む), `on_chat_model_end`, `on_chain_end` などのイベントがコンソールにストリーミング表示されるはずです。