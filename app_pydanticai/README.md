# PydanticAI Chat Application

PydanticAIは、FastAPIバックエンドとNext.jsフロントエンドを組み合わせたAIチャットアプリケーションです。Pydanticを活用した型安全なAPI設計と、ストリーミング対応のチャットインターフェースを提供します。

## 主な機能
- **AIエージェントとの対話**
  - リアルタイムチャットインターフェース
  - ストリーミングレスポンス
  - 会話履歴の管理

- **型安全なAPI設計**
  - Pydanticモデルを使用したリクエスト/レスポンスのバリデーション
  - OpenAPI仕様の自動生成

- **拡張可能なアーキテクチャ**
  - 新しいAIエージェントの追加が容易
  - カスタムAPIエンドポイントの統合

## 技術スタック

### バックエンド
- Python 3.10+
- FastAPI
- Pydantic
- OpenAI API

### フロントエンド
- Next.js
- TypeScript
- Tailwind CSS

## ディレクトリ構成

```
app_pydanticai/
├── backend/            # バックエンド実装
│   ├── api.py          # APIエンドポイント
│   └── agents/         # AIエージェント実装
├── frontend/           # フロントエンド実装
│   ├── src/            # ソースコード
│   │   ├── app/        # Next.jsアプリケーションページ
│   │   ├── components/ # UIコンポーネント
│   │   └── types/      # TypeScript型定義
│   └── public/         # 静的アセット
```

## 使用方法

1. 開発用の個別起動
- バックエンドサーバー:
```bash
docker compose up dev_backend
```
- フロントエンドサーバー:
```bash
docker compose up dev_frontend
```

1. ブラウザで以下にアクセス
- フロントエンドUI: http://localhost:8081
- バックエンドAPI: http://localhost:8080
