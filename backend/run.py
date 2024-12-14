from app import create_app
from app.database import db

app = create_app()

# 必要ならば、初回実行時にDB作成
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=50000)
