CREATE TABLE stocks (
    stock_id INT AUTO_INCREMENT PRIMARY KEY,      -- 主キー、自動インクリメント
    symbol VARCHAR(10) NOT NULL,                  -- ティッカーシンボル、NULL不可
    purchase_price DECIMAL(10,2) NOT NULL,        -- 取得単価
    quantity INT NOT NULL,                        -- 保有株数
    target_price DECIMAL(10,2),                   -- 売却目標価格
    cutloss_price DECIMAL(10,2),                  -- 損切り価格
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 登録日時、デフォルトで現在日時
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP  -- 更新日時、更新時に自動更新
);
