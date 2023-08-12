#!/bin/bash

# pipenvがインストールされているか確認。なければインストール。
if ! command -v pipenv &> /dev/null; then
    pip install pipenv
fi

# プロジェクトのディレクトリに移動
cd ./server/app || { echo "ディレクトリの移動に失敗しました。"; exit 1; }

# Pipfileからの依存関係のインストール
pipenv install

# マイグレーションの実行
pipenv run python manage.py makemigrations
pipenv run python manage.py migrate

# Djangoの開発サーバーの起動
pipenv run python manage.py runserver
