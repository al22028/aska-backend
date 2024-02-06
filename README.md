# aska-backend

![python](https://img.shields.io/badge/-Python-F2C63C.svg?logo=python&style=for-the-badge) ![AWS](https://img.shields.io/badge/Amazon_AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white) ![lambda](https://img.shields.io/badge/-AWS%20lambda-232F3E.svg?logo=aws-lambda&style=for-the-badge) ![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white) ![git](https://img.shields.io/badge/GIT-E44C30?style=for-the-badge&logo=git&logoColor=white) ![github-actions](https://img.shields.io/badge/-githubactions-FFFFFF.svg?logo=github-actions&style=for-the-badge)
![postgresql](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white) ![terraform](https://img.shields.io/badge/-terraform-20232A?style=for-the-badge&logo=terraform&logoColor=844EBA)

## Versions

使用している言語やソフトウェアのバージョン情報

| 言語・フレームワーク | バージョン |
| -------------------- | ---------- |
| Python               | 3.11.6     |
| volta                | 1.1.1      |
| Node.js              | v18.12.1   |
| npm                  | 8.19.2     |
| Docker               | ^4.20.0    |

## Installation

`pyenv`を使って`Python`のバージョン合わせる場合は[こちらの記事](https://qiita.com/twipg/items/75fc9428e4c33ed429c0)を参考に`Python 3.11.6`を使用してください。

```bash
# install poetry
pip install poetry
# Poetry to use project-specific virtual env
poetry config virtualenvs.in-project true
# install virtual env
poetry install
# install npm dependencies
npm install
```

## Usage

### Docker

```bash
# コンテナの立ち上げ (フォアグランド)
docker compose up
# コンテナの立ち上げ (バックグラウンド)
docker compose up -d
```

### Task Runner

#### Python

```bash
# migration
poetry run task migrate
# format
poetry run task format
# lint
poetry run task lint
# pytest
poetry run task test
```

#### npm

```bash
# run local api server (use .vnev interpreter)
npm run dev
# clean up cache dirs
npm run clean
```

### Run local server

health check 用エンドポイント: <http://localhost:3333/local/api/v1/health>

```bash
# activate python venv shell
poetry shell
# run local api server (serverless offline)
npm run dev
```

### Migrations

参考：<https://qiita.com/penpenta/items/c993243c4ceee3840f30>

```bash
cd src/v1
# 新しくモデルを追加した場合
alembic revision --autogenrate -m "migration message"
# データベースに最新のマイグレーションを反映
alembic upgrade head
```

### Terraform

```bash
cd terraform/environment/dev
terraform apply
```

## Branch

基本的には [Git-flow](https://qiita.com/KosukeSone/items/514dd24828b485c69a05 "Git-flowって何？") です

### Branch naming rule

| ブランチ名                   | 説明             | 補足 |
| ---------------------------- | ---------------- | ---- |
| main                         | 最新リリース     |      |
| dev/main                     | 開発用最新       |
| hotfix/{モジュール名}/{主題} |
| sandbox/{なんでも}           | テストコードなど |

### Branch rule

- 作業は各最新ブランチから分岐させる
- 作業ブランチはマージ後に削除
- できるだけレビューする(誰かにしてもらう)
- ビルドやデプロイなどは別途検討

### Commit message

Please refer to the following template for the commit message.

```plaintext
🐞 バグとパフォーマンス
#🐛 :bug: バグ修正
#🚑 :ambulance: 重大なバグの修正
#🚀 :rocket: パフォーマンス改善
#💻 コードの品質とスタイル
#👍 :+1: 機能改善
#♻️ :recycle: リファクタリング
#👕 :shirt: Lintエラーの修正やコードスタイルの修正

🎨 UI/UXとデザイン
#✨ :sparkles: 新しい機能を追加
#🎨 :art: デザイン変更のみ

🛠️ 開発ツールと設定
#🚧 :construction: WIP (Work in Progress)
#⚙ :gear: config変更
#📦 :package: 新しい依存関係追加
#🆙 :up: 依存パッケージなどのアップデート

📝 ドキュメントとコメント
#📝 :memo: 文言修正
#📚 :books: ドキュメント
#💡 :bulb: 新しいアイデアやコメント追加

🛡️ セキュリティ
#👮 :op: セキュリティ関連の改善

🧪 テストとCI
#💚 :green_heart: テストやCIの修正・改善

🗂️ ファイルとフォルダ操作
#📂 :file_folder: フォルダの操作
#🚚 :truck: ファイル移動

📊 ログとトラッキング
#💢 :anger: コンフリクト
#🔊 :loud_sound: ログ追加
#🔇 :mute: ログ削除
#📈 :chart_with_upwards_trend: アナリティクスやトラッキングコード追加

💡 その他
#🧐 :monocle_face: コードのリーディングや疑問
#🍻 :beers: 書いているときに楽しかったコード
#🙈 :see_no_evil: .gitignore追加
#🛠️ :hammer_and_wrench: バグ修正や基本的な問題解決
```
