import mesop as mp
import pymongo
import os

# MongoDBクライアントの初期化
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = pymongo.MongoClient(MONGO_URI)
db = client["baseline_db"]
collection = db["frontend_states"]

def check_backend_connection():
    try:
        # バックエンドへの接続確認（実際のAPIエンドポイントに変更）
        import requests
        response = requests.get("http://backend:8000/health")
        return response.json()['status'] == 'healthy'
    except Exception:
        return False

def save_state(state: str):
    try:
        collection.insert_one({"state": state})
        return True
    except Exception as e:
        print(f"状態保存エラー: {e}")
        return False

def get_last_state():
    try:
        last_state = collection.find_one(sort=[("_id", pymongo.DESCENDING)])
        return last_state['state'] if last_state else "未保存"
    except Exception as e:
        print(f"状態取得エラー: {e}")
        return "エラー"

# グローバル変数として状態を保持
state_input_value = ""

def on_input_change(value: str):
    global state_input_value
    state_input_value = value

def on_save():
    global state_input_value
    if save_state(state_input_value):
        mp.toast("状態を正常に保存しました")
    else:
        mp.toast("状態の保存に失敗しました")

@mp.page()
def app():
    backend_status = "接続済み" if check_backend_connection() else "未接続"
    last_state = get_last_state()
    
    mp.text("Mesopベースラインアプリケーション")
    mp.text(f"バックエンド状態: {backend_status}")
    mp.text(f"最後の保存状態: {last_state}")
    
    mp.input(
        label="状態を入力", 
        on_change=on_input_change
    )
    
    mp.button("状態を保存", on_click=on_save)

def main():
    mp.run(app)

if __name__ == "__main__":
    main()
