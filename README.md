# Python開発ベースライン

## プロジェクト概要
このプロジェクトは、Pythonを使用したウェブアプリケーションのベースラインテンプレートです。

## 必要な環境
- Docker
- Docker Compose
- Visual Studio Code
- Dev Containers拡張機能

## 開発環境（.devcontainer）
このプロジェクトは、VS Code Dev Containersを使用して一貫した開発環境を提供します。

### 開発環境の特徴
- **Python 3.12**: 最新のPython環境
- **UV パッケージマネージャー**: 高速なPythonパッケージインストール
- **Docker outside of Docker**: コンテナ内でのDocker実行環境
- **AWS CLI**: AWSリソース管理用ツール
- **事前設定済みVS Code拡張機能**:
  - Git Graph: Gitの履歴可視化
  - Claude Dev: AI支援開発
  - Markdown Preview Enhanced: Markdownプレビュー
  - Markdown All in One: Markdown編集支援
  - Jupyter: Jupyter Notebook支援
  - Python Environment Manager: Python環境管理

### 開発環境の使用方法
1. VS Codeで「Dev Containers」拡張機能をインストール
2. プロジェクトフォルダをVS Codeで開く
3. コマンドパレット（F1）から「Dev Containers: Reopen in Container」を選択
4. 開発コンテナのビルドと起動が自動的に行われます

### ネットワーク設定
- 開発環境は`devnet`という専用のDockerネットワークで実行
- 他のコンテナとの連携が容易

## 注意点
- AWS認証情報を使用する場合は、ホストの`~/.aws`ディレクトリがコンテナにマウントされます
