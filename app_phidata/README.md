# Phidata Chat Application

Phidataは、FastAPIバックエンドとMesopフロントエンドを組み合わせたチャットアプリケーションです。AIエージェントとの対話を可能にし、複数のAPIモードをサポートしています。

## 主な機能

- **3つのAPIモード**
  - 通常レスポンスモード
  - ストリーミングレスポンスモード
  - メッセージストリーミングモード

- **インタラクティブなUI**
  - リアルタイムチャットインターフェース
  - ストリーミング表示
  - APIモード切り替え機能
  - サンプルメッセージの表示

- **拡張可能なアーキテクチャ**
  - 新しいAPIエンドポイントの追加が容易
  - カスタムエージェントの統合が可能

## 技術スタック

### バックエンド
- Python 3.10+
- FastAPI
- Pydantic
- SSE (Server-Sent Events)

### フロントエンド
- Mesop
- TypeScript
- Tailwind CSS

## ディレクトリ構成

```
app_phidata/
├── backend/            # バックエンド実装
│   ├── api.py          # APIエンドポイント
│   └── agents/         # AIエージェント実装
├── frontend/           # フロントエンド実装
│   ├── main.py         # メインアプリケーション
│   ├── data_model.py   # データモデル定義
│   ├── dialog.py       # UIコンポーネント
│   └── api_client.py   # APIクライアント
```

## 使用方法

1. バックエンドサーバーの起動
```bash
docker compose up dev_backend
```
バックエンドはポート8080で起動します

2. フロントエンドサーバーの起動
```bash
docker compose up dev_frontend
```
フロントエンドはポート8081で起動します

3. ブラウザで以下にアクセス
- バックエンドAPI: http://localhost:8080
- フロントエンドUI: http://localhost:8081
