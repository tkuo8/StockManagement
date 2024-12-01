from flask import current_app
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from contextlib import contextmanager

@contextmanager
def get_db():
    """
    データベースセッションを管理するジェネレーター関数。
    リクエストごとに新しいセッションを提供し、終了後にセッションを閉じる。
    """
    with current_app.app_context():
        
        # SQLAlchemyのエンジン作成
        engine = create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'], echo=True)

        # セッションメーカー
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        db = SessionLocal()  # 新しいセッション
        try:
            yield db  # セッションを渡す
        finally:
            db.close()  # セッションを閉じる
