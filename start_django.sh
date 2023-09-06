#!/bin/bash

# pipenvがインストールされているか確認。なければインストール。
if ! command -v pipenv &> /dev/null; then
    pip install pipenv
fi

# プロジェクトのディレクトリに移動
cd ./server/app || { echo "ディレクトリの移動に失敗しました。"; exit 1; }

if [ -e .env.sample ]; then
    cp .env.sample .env
fi

# データベースの削除
rm -rf db.sqlite3

# Pipfileからの依存関係のインストール
pipenv install
pipenv install --dev

# 設定の更新
export DJANGO_SETTINGS_MODULE=config.settings.dev

# マイグレーションの実行
pipenv run python manage.py makemigrations
pipenv run python manage.py migrate

# テストデータの作成
pipenv run python manage.py loaddata accounts/fixtures/data.json campuses/fixtures/data.json items/fixtures/data.json

# Djangoの開発サーバーの起動
pipenv run python manage.py runserver
