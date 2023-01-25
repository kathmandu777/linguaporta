# linguaporta

## Overview
linguaportaを自動で解答するためのスクリプト+サーバー(DB)です。

### 対応している問題
- 単語の意味
- 空所補充

## 初心者向けの使い方
1. pythonの環境構築
2. リポジトリをクローン
    ```sh
    git clone https://github.com/kathmandu777/linguaporta.git
    ```
3. `bot/requirements.txt` に書かれているライブラリをインストール
    ```sh
    pip install -r bot/requirements.txt
    ```
4. 自分のブラウザのドライバーをダウンロード (バージョンに注意)
5. `CHROMEDRIVER` 変数にドライバーのパスを設定
6. `bot/main.py` を実行
    ```sh
    python bot/main.py
    ```

## For Developers
### Prerequisites

#### Poetry

Dependency management for Python files is done using POETRY.

1. <https://python-poetry.org/docs/#installation>
1. `python -m venv venv`
1. `source venv/bin/activate`
1. `pip install --upgrade pip` (if needed)
1. `poetry install` (After cloning this repository)

#### pre-commit (for developers)

This tool defines commands to be executed before committing. It is already defined in `.pre-commit-config.yaml`, so you need to configure it in your environment. Please follow the steps below.

1. <https://pre-commit.com/#installation>
1. `pre-commit install` (After cloning this repository)

### Usage (Local Server)

1. Clone this repository

1. Create fastapi.env with reference to fastapi.env.tmpl

1. Start Server

    ```sh
    docker-compose up
    ```

1. Run bot/main.py
   ```sh
   python bot/main.py
   ```

#### Additional commands
- Dependency install

    ```sh
    docker-compose run --rm fastapi poetry install
    ```

- Setup Static Files

    ```sh
    docker-compose run --rm fastapi poetry run python manage.py collectstatic --noinput
    ```

- Migrate

    ```sh
    docker-compose run --rm fastapi poetry run python manage.py migrate
    ```

- Create Super User for Admin Page

    ```sh
    docker-compose run --rm fastapi poetry run python manage.py createsuperuser
    ```

### Alias for frequently used commands

```sh
source alias.sh
```
