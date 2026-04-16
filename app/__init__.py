import os
import sqlite3
from flask import Flask

def create_app(test_config=None):
    # 初始化 Flask app，並設定 instance 目錄來存放本機 DB
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev_key'),
        DATABASE=os.path.join(app.instance_path, 'database.db'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # 確保 instance folder 存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 統一註冊 Router (Blueprints)
    from .routes import main_bp, auth_bp, review_bp, admin_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(review_bp)
    app.register_blueprint(admin_bp)

    return app

def init_db(app=None):
    """
    提供給命令列執行的初始化 DB 指令
    用法範例： python -c "from app import create_app, init_db; init_db(create_app())"
    """
    if app is None:
        from flask import current_app
        app = current_app
        
    db_path = app.config['DATABASE']
    schema_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'schema.sql')
    
    with sqlite3.connect(db_path) as conn:
        with open(schema_path, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
            
    print(f"資料庫結構已經初始化至: {db_path}")
