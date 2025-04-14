# sse_client.py
import httpx
import json
import asyncio

async def main():
    """Connects to the SSE endpoint and prints received events."""
    print("Connecting to SSE endpoint http://127.0.0.1:8000/stream_events ...")
    # リクエストボディを定義
    request_data = {
        "input": "Tell me a short story about a brave knight.",
        "config": {"llm_model_name": "gpt-3.5-turbo"} # モデルを指定しても良い
    }
    print(f"Sending request with input: '{request_data['input']}'")

    try:
        # httpxを使って非同期に接続
        async with httpx.AsyncClient(timeout=None) as client: # タイムアウトなし
            # POSTリクエストでストリーム接続を開始
            async with client.stream(
                "POST",
                "http://127.0.0.1:8000/stream_events",
                json=request_data
            ) as response:
                print(f"Server Response Status Code: {response.status_code}")

                # ステータスコードが200 OKか確認
                if response.status_code == 200:
                    print("--- Streaming Events Start ---")
                    # レスポンスの各行を非同期に処理
                    async for line in response.aiter_lines():
                        line = line.strip() # 前後の空白を削除
                        if line: # 空行は無視
                            print(line) # 受信した行をそのまま出力
                            # 必要に応じてイベント名とデータをパースして表示
                            # if line.startswith("event:"):
                            #     event_name = line[len("event:"):].strip()
                            #     print(f"Received event name: {event_name}")
                            # elif line.startswith("data:"):
                            #     data_content = line[len("data:"):].strip()
                            #     print(f"Received data string: {data_content}")
                            #     try:
                            #         # JSONとしてパース試行
                            #         data_json = json.loads(data_content)
                            #         print(f"Parsed data JSON: {data_json}")
                            #     except json.JSONDecodeError:
                            #         print("Data is not valid JSON.")
                    print("--- Streaming Events End ---")
                else:
                    # エラーレスポンスの場合
                    print(f"Error: Received status code {response.status_code}")
                    error_content = await response.aread() # エラー内容を読み込む
                    print("Error response content:")
                    print(error_content.decode()) # バイト列をデコードして表示

    except httpx.ConnectError as e:
        # 接続エラーの場合
        print(f"Connection Error: Could not connect to the server. Is it running? Details: {e}")
    except Exception as e:
        # その他の予期せぬエラー
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # 非同期関数を実行
    asyncio.run(main())