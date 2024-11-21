## **株管理アプリ 外部設計書**

### **1. システム概要**

本システムは、ユーザーが複数の株を効率的に管理できるよう、株の情報登録・管理、目標達成度の可視化、株価履歴管理、取引履歴の記録、およびアラート通知機能を提供します。また、外部 API を使用してリアルタイムの株価更新をサポートします。

---

### **2. インターフェース設計**

#### **2.1 ユーザーインターフェース（UI）**

ユーザーインターフェースは React を使用して構築され、直感的に操作できるデザインを採用しています。主な画面は以下の通りです：

- **株情報管理画面**  
  ユーザーが保有する株式を登録、編集、削除する画面。銘柄シンボル、購入価格、株数、目標価格、損切り価格などを入力して管理します。

- **株価閲覧画面**  
  各株式の最新株価および価格変動を表示する画面。

- **目標達成状況画面**  
  設定した目標価格や損切り価格に対する進捗をグラフで可視化。

- **取引履歴画面**  
  株式の売買履歴を時系列で一覧表示。

- **アラート通知画面**  
  設定した目標価格や損切り価格に達した場合の通知を一覧表示。

---

#### **2.2 API インターフェース**

外部 API を利用して株価情報や分析指標を取得します：

- **Yahoo Finance API**: 株価および過去の株価データの取得。
- **Alpha Vantage API**: テクニカル指標（MACD、RSI）の取得。

##### **サンプル API 設計**

以下は Yahoo Finance API を利用した株価取得の例です：

- **エンドポイント**: `https://query1.finance.yahoo.com/v7/finance/quote`
- **リクエストパラメータ**:
  - `symbols`: 銘柄シンボル（例: "AAPL"）
- **レスポンス形式**: JSON
- **レスポンス例**:
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

---

#### **2.3 データベース設計**

データベースは MySQL を使用します。テーブル設計は以下の通りです：

##### **users テーブル**

| カラム名          | データ型     | 備考                       |
| ----------------- | ------------ | -------------------------- |
| `user_id`         | INT (PK)     | ユーザー ID                |
| `email`           | VARCHAR(255) | メールアドレス             |
| `password_hash`   | VARCHAR(255) | ハッシュ化されたパスワード |
| `username`        | VARCHAR(100) | ユーザー名                 |
| `registered_date` | DATETIME     | アカウント作成日時         |

##### **stocks テーブル**

| カラム名          | データ型      | 備考                       |
| ----------------- | ------------- | -------------------------- |
| `stock_id`        | INT (PK)      | 銘柄 ID                    |
| `user_id`         | INT (FK)      | ユーザー ID                |
| `symbol`          | VARCHAR(10)   | 銘柄シンボル（例: "AAPL"） |
| `purchase_price`  | DECIMAL(10,2) | 購入価格                   |
| `quantity`        | INT           | 保有株数                   |
| `target_price`    | DECIMAL(10,2) | 目標価格                   |
| `stop_loss_price` | DECIMAL(10,2) | 損切り価格                 |
| `created_at`      | DATETIME      | 登録日時                   |

##### **stock_history テーブル**

| カラム名     | データ型      | 備考     |
| ------------ | ------------- | -------- |
| `history_id` | INT (PK)      | 履歴 ID  |
| `stock_id`   | INT (FK)      | 銘柄 ID  |
| `price`      | DECIMAL(10,2) | 市場価格 |
| `date`       | DATETIME      | 記録日   |

##### **transaction_history テーブル**

| カラム名           | データ型       | 備考     |
| ------------------ | -------------- | -------- |
| `transaction_id`   | INT (PK)       | 取引 ID  |
| `stock_id`         | INT (FK)       | 銘柄 ID  |
| `transaction_type` | ENUM(BUY/SELL) | 売買種別 |
| `price`            | DECIMAL(10,2)  | 取引価格 |
| `quantity`         | INT            | 取引株数 |
| `transaction_date` | DATETIME       | 取引日   |

---

#### **2.4 バックエンド API 設計**

バックエンドは Java + Spring Boot を使用して構築されます。主な API の例：

- **株情報登録 API**

  - **エンドポイント**: `POST /api/stocks`
  - **リクエスト例**:
    ```json
    {
      "symbol": "AAPL",
      "purchase_price": 145.5,
      "quantity": 100,
      "target_price": 150.0,
      "stop_loss_price": 140.0
    }
    ```
  - **レスポンス例**:
    ```json
    {
      "stock_id": 1,
      "symbol": "AAPL",
      "purchase_price": 145.5,
      "quantity": 100,
      "target_price": 150.0,
      "stop_loss_price": 140.0
    }
    ```

- **株価履歴取得 API**
  - **エンドポイント**: `GET /api/stocks/{stock_id}/history`
  - **レスポンス例**:
    ```json
    [
      {
        "date": "2024-11-20",
        "price": 150.1
      },
      {
        "date": "2024-11-19",
        "price": 148.2
      }
    ]
    ```

---

### **3. セキュリティ設計**

- **JWT 認証**: 各 API の利用時に JWT トークンを使用して認証を行います。
- **パスワードハッシュ化**: パスワードはハッシュ化して保存（例: bcrypt）。

---

### **4. アラート通知**

- **通知トリガー**: 株価が目標価格または損切り価格に達した際に通知。
- **通知方法**: WebSocket を利用したリアルタイム通知。
