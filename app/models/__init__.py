import sqlite3
import os
from flask import current_app

def get_db_connection():
    """
    獲取與本機 SQLite 資料庫的連線。
    
    使用 Flask current_app 的 config 來取的正確的 DATABASE 路徑，
    並設定 row_factory = sqlite3.Row，讓後續取出的資料能像 Dictionary 一樣透過鍵名稱取值。
    
    Returns:
        sqlite3.Connection: 資料庫連線物件
    """
    try:
        db_path = current_app.config['DATABASE']
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"資料庫連線發生錯誤: {e}")
        # 將錯誤向上拋出，以利外層的路由抓取與給予 500 回應
        raise
