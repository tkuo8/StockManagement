CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,      -- 主キー、自動インクリメント
    username VARCHAR(255) NOT NULL UNIQUE,       -- ユーザー名、ユニーク、NULL不可
    password VARCHAR(255) NOT NULL,              -- ハッシュ化されたパスワード、NULL不可
    email VARCHAR(255) NOT NULL UNIQUE,          -- メールアドレス、ユニーク、NULL不可
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- アカウント作成日時、デフォルトで現在日時
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP  -- 情報更新日時、更新時に自動更新
);
