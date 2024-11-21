### 株管理アプリ 外部設計書

#### 1. **システム概要**

本システムは、ユーザーが複数の株を効率的に管理するために、株の情報登録・管理、目標達成度の可視化、テクニカル分析、アラート機能などを提供します。また、外部 API を使用して株価やテクニカル指標の情報を取得し、リアルタイムでの株価更新をサポートします。

#### 2. **インターフェース設計**

##### 2.1 **ユーザーインターフェース（UI）**

ユーザーインターフェースは React を使用して構築され、シンプルかつ直感的に操作できるようにデザインされます。UI は以下の要素で構成されます：

- **株情報管理画面**: ユーザーが保有株を登録・編集・削除できる画面。銘柄名、購入価格、株数、目標額などを入力し、管理します。
- **株価・指標閲覧画面**: 最新の株価やテクニカル指標（MACD、RSI など）を表示する画面。
- **目標達成状況管理画面**: 目標設定とその達成度をグラフやチャートで表示。
- **アラート通知画面**: アラート通知を表示し、株価や損切りラインに達した際のリアルタイム通知。
- **配当管理画面**: 配当金情報を管理し、トータル利益に反映。

##### 2.2 **API インターフェース**

システムは外部 API を利用して、株価、過去データ、テクニカル指標を取得します。

- **Yahoo Finance API**: 株価および過去の株価データを取得します。リクエストは以下のエンドポイントを通じて行います：

  - エンドポイント：`https://query1.finance.yahoo.com/v7/finance/quote`
  - パラメータ：
    - `symbols`: 銘柄シンボル（例: "AAPL"）
  - レスポンス形式：JSON
  - レスポンス例：
    ```json
    {
      "quoteResponse": {
        "result": [
          {
            "symbol": "AAPL",
            "regularMarketPrice": 150.1,
            "regularMarketChangePercent": 1.2
          }
        ]
      }
    }
    ```

- **Alpha Vantage API**: テクニカル指標（MACD、RSI など）を取得します。以下のエンドポイントを使用：

  - エンドポイント：`https://www.alphavantage.co/query`
  - パラメータ：
    - `function`: `MACD` または `RSI`
    - `symbol`: 銘柄シンボル（例: "AAPL"）
    - `interval`: `1min`, `5min`, `15min`, etc.
    - `apikey`: API キー
  - レスポンス形式：JSON
  - レスポンス例：
    ```json
    {
      "Technical Analysis: MACD": {
        "2018-12-27 16:00:00": {
          "MACD": "1.03",
          "Signal": "0.98"
        }
      }
    }
    ```

- **Quandl API**: 経済指標や株価データを取得します。以下のエンドポイントを使用：
  - エンドポイント：`https://www.quandl.com/api/v3/datasets/WIKI/AAPL.json`
  - パラメータ：
    - `api_key`: API キー
  - レスポンス形式：JSON
  - レスポンス例：
    ```json
    {
      "dataset": {
        "data": [["2020-01-01", 300.1]]
      }
    }
    ```

##### 2.3 **データベース設計**

データは MySQL で管理されます。以下のテーブルを使用してデータを格納します：

- **users テーブル**

  - `id`: ユーザー ID（主キー）
  - `username`: ユーザー名
  - `email`: メールアドレス
  - `password`: ハッシュ化されたパスワード
  - `created_at`: アカウント作成日時

- **stocks テーブル**

  - `id`: 株情報 ID（主キー）
  - `user_id`: ユーザー ID（外部キー）
  - `symbol`: 銘柄シンボル（例: "AAPL"）
  - `purchase_price`: 購入価格
  - `quantity`: 株数
  - `target_price`: 目標価格
  - `created_at`: 登録日時

- **transactions テーブル**
  - `id`: 取引 ID（主キー）
  - `user_id`: ユーザー ID（外部キー）
  - `stock_id`: 株 ID（外部キー）
  - `type`: 取引タイプ（"buy" または "sell"）
  - `price`: 取引価格
  - `quantity`: 取引株数
  - `created_at`: 取引日時

##### 2.4 **バックエンド API**

バックエンドは Java + Spring Boot を使用して構築され、RESTful API を提供します。主なエンドポイントは以下の通りです：

- **株情報登録 API**

  - エンドポイント：`POST /api/stocks`
  - リクエストボディ：
    ```json
    {
      "symbol": "AAPL",
      "purchase_price": 145.5,
      "quantity": 100,
      "target_price": 150.0
    }
    ```
  - レスポンス：
    ```json
    {
      "id": 1,
      "symbol": "AAPL",
      "purchase_price": 145.5,
      "quantity": 100,
      "target_price": 150.0
    }
    ```

- **株情報取得 API**

  - エンドポイント：`GET /api/stocks/{id}`
  - レスポンス：
    ```json
    {
      "id": 1,
      "symbol": "AAPL",
      "purchase_price": 145.5,
      "quantity": 100,
      "target_price": 150.0
    }
    ```

- **株価更新 API**
  - エンドポイント：`GET /api/stocks/{id}/updatePrice`
  - レスポンス：
    ```json
    {
      "current_price": 150.1,
      "percentage_change": 1.2
    }
    ```

#### 3. **セキュリティ設計**

- **JWT 認証**: ユーザー認証には JWT を使用し、セッション管理を行います。ログイン時にトークンを発行し、その後のリクエストにトークンを添付して認証を行います。

#### 4. **アラート機能**

ユーザーに株価が目標価格に達した際や損切りラインに達した際に、リアルタイムでアラートを通知します。通知は WebSocket または定期的なポーリングを通じて行います。
