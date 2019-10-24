# blog_crawler

## Setup
Docker イメージをビルドします

```bash
$ docker-compose build
```

## Usage

### Run crawler

以下のコマンドで scrapy で実装されたクローラーを起動します
クローラーの引数には、クロール対象の企業名とブログトップページの URL を指定します

```bash
$ docker-compose run crawler scrapy crawl site_crawl -a company_name='<企業名>' -a url=<ブログトップページのURL>
```

### Execute query in database

PostgreSQL に保存されたデータは `psql` を利用して確認できます

```bash
# postgres のコンテナ内で psql を起動する
$ docker-compose exec postgres psql -U docker -d crawler

# psql のコンソールで SQL を実行できます
# psql (11.2 (Debian 11.2-1.pgdg90+1))
# Type "help" for help.
#
# crawler=# select * from articles limit 10;
# ...
```