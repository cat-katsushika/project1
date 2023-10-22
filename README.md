# 初期設定
## `.env`ファイルを作成する(環境構築の際に必要な設定)
カレントディレクトリ: server
```
$ make dev-env
```

# 環境構築
## Dockerイメージの作成とDockerコンテナの起動(ローカルサーバーの起動)
カレントディレクトリ: server
```
$ make dev
```

## テストデータの作成 (fixtures.yamlから生成)
カレントディレクトリ: server

前提条件: Dockerコンテナ起動中
```
$ make fixtures
```
### 作成されるデータ
管理画面アクセス可ユーザー
```
email: admin@example.com
password: admin
```
その他ユーザー
```
email: test1@example.com
password: test
```
