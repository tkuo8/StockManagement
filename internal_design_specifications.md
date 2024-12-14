## **株管理アプリ 内部設計書**

### **1. システム概要**

本システムは、株式投資ユーザーの効率的な管理と投資支援を目的としており、以下の主要機能を提供します：

- 株情報の登録・編集・削除
- 目標達成度の可視化と進捗管理
- テクニカル指標を活用した売買タイミングの分析
- 外部 API を使用したリアルタイム株価更新
- アラート通知による迅速な対応支援
- 保有株の状態管理（保有中・買い時・売り時等）

---

### **2. 詳細設計**

#### **2.1 データベース設計**

**1. 保有株情報テーブル (stocks)**

- **テーブル名**: `stocks`
- **主キー**: `stock_id`
- **カラム定義**:
  - `stock_id`: INT (AUTO_INCREMENT, PRIMARY KEY)
  - `symbol`: VARCHAR(10) (銘柄シンボル)
  - `purchase_price`: DECIMAL(10,2) (購入価格)
  - `quantity`: INT (保有数量)
  - `target_price`: DECIMAL(10,2) (目標価格)
  - `stop_loss_price`: DECIMAL(10,2) (損切り価格)
  - `status`: ENUM ("holding", "watching", "buy", "sell", "disabled") (状態)
  - `created_at`: DATETIME (登録日時)
  - `updated_at`: DATETIME (更新日時)

**2. 取引履歴テーブル (transactions)**

- **テーブル名**: `transactions`
- **主キー**: `transaction_id`
- **カラム定義**:
  - `transaction_id`: INT (AUTO_INCREMENT, PRIMARY KEY)
  - `stock_id`: INT (外部キー, `stocks.stock_id`)
  - `transaction_type`: ENUM ("buy", "sell")
  - `price`: DECIMAL(10,2) (取引価格)
  - `quantity`: INT (取引数量)
  - `profit_loss`: DECIMAL(10,2) (損益額)
  - `transaction_date`: DATETIME (取引日時)

**3. 目標進捗テーブル (goal_progress)**

- **テーブル名**: `goals`
- **主キー**: `goal_id`
- **カラム定義**:
  - `goal_id`: INT (AUTO_INCREMENT, PRIMARY KEY)
  - `traded_at`: DATE (取引日)
  - `progress_rate`: DECIMAL(5,2) (進捗率)
  - `period`: INT (外部キー, `goal_periods.period_id`)
  - `created_at`: DATETIME (登録日時)
  - `updated_at`: DATETIME (更新日時)

**4. 目標期間テーブル (goal_periods)**

- **テーブル名**: `goal_periods`
- **主キー**: `period_id`
- **カラム定義**:
  - `period_id`: INT (AUTO_INCREMENT, PRIMARY KEY)
  - `target_amount`: DECIMAL(10,2) (目標額)
  - `started_at`: DATE (期間開始日)
  - `ended_at`: DATE (期間終了日)
  - `created_at`: DATETIME (登録日時)
  - `updated_at`: DATETIME (更新日時)

---

#### **2.2 バックエンド API 設計**

**1. 株情報管理 API**

- **株情報登録 API**
  - **エンドポイント**: `POST /api/stocks`
  - **リクエスト例**:
    ```json
    {
      "symbol": "AAPL",
      "purchase_price": 145.5,
      "quantity": 100,
      "target_price": 150.0,
      "stop_loss_price": 140.0,
      "status": "holding"
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
      "stop_loss_price": 140.0,
      "status": "holding"
    }
    ```

**2. 株価取得 API**

- **エンドポイント**: `GET /api/stock-price/{symbol}`
  - **レスポンス例**:
    ```json
    {
      "symbol": "AAPL",
      "current_price": 148.2
    }
    ```

**3. テクニカル指標 API**

- **エンドポイント**: `GET /api/indicators/{symbol}`
  - **レスポンス例**:
    ```json
    {
      "symbol": "AAPL",
      "macd": 1.25,
      "rsi": 45.8
    }
    ```

---

#### **2.3 ロジック設計**

**1. 株価進捗計算ロジック**

- **概要**: 現在の株価を基に、目標価格と損切り価格までの進捗率を計算します。
- **アルゴリズム**:
  - 進捗率 = ((現在株価 - 購入価格) / (目標価格 - 購入価格)) × 100
  - 損切り価格以下の場合、負の進捗率を返す。

**2. アラート判定ロジック**

- **概要**: 現在の株価が目標価格または損切り価格に近づいた場合にアラートを生成。
- **条件**:
  - (目標価格 - 現在株価) / 目標価格 ≤ 0.05
  - (現在株価 - 損切り価格) / 損切り価格 ≤ 0.05

**3. テクニカル指標トリガーロジック**

- **概要**: MACD とシグナルの交差点を検知し、上昇トレンド開始のサインを識別。
- **アルゴリズム**:
  - MACD 値がシグナルを上回るタイミングでフラグを設定。
  - 上昇トレンドフラグが立った銘柄をリストに追加。

---

#### **2.4 レイアウト設計**

**1. 株情報管理画面**

- **目的**: 銘柄の登録、編集、削除を管理。
- **構成要素**:
  - 銘柄一覧テーブル: 銘柄シンボル、購入価格、目標価格、損切り価格、保有状態を表示。
  - 登録・編集モーダル: 入力フィールド（シンボル、購入価格、数量、目標価格、損切り価格）。

**2. 株価閲覧画面**

- **目的**: 株価やテクニカル指標の視覚化。
- **構成要素**:
  - 株価チャート: `Chart.js` を使用。
  - テクニカル指標カード: MACD、RSI、移動平均線の数値を表示。

**3. 目標達成状況画面**

- **目的**: ユーザーの目標達成状況を把握。
- **構成要素**:
  - 進捗バー: プログレスバーで進捗を表示。
  - 達成度グラフ: 棒グラフまたは円グラフで全体の達成率を表示。

**4. 取引履歴画面**

- **目的**: 売買履歴の管理と表示。
- **構成要素**:
  - 履歴一覧テーブル: 日時、取引種別、価格、数量、損益額を表示。

**5. アラート通知画面**

- **目的**: アラートの一覧表示。
- **構成要素**:
  - アラート一覧: 条件に一致した銘柄と通知内容を表示。
  - フィルタ機能: 重要度や状態で絞り込み可能。

---

### **3. 技術仕様**

- **フロントエンド**: React, Bootstrap, Chart.js
- **バックエンド**: Python (Flask)
- **データベース**: MySQL
- **外部サービス**: Yahoo Finance API, Alpha Vantage API
- **CI/CD**: GitHub Actions
