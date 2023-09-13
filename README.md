### apiサーバーの起動

bashが使える環境(linux, mac, wslとか)で
```bash:
./start_django.sh
```
を実行する

### テストデータ
上記./start_django.shの実行と共に作成される。
```
管理画面ログイン用
email: admin@ed.tus.ac.jp
password: admin
```
```
テストユーザー
email: example@ed.tus.ac.jp
password: example
```

### swaggerの参照
上記のapiサーバーの立ち上げを行った上で、下記URLから参照可能。
```
http://127.0.0.1:8000/api/schema/swagger-ui/
```
