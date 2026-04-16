import sqlite3
import os

def get_db_connection():
    """
    獲取與 SQLite 資料庫的連線
    並設定 row_factory 使得查詢結果可以像 dict 一樣依據欄位名稱存取
    """
    # 預設把 DB 開在專案根目錄的 instance/database.db
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    instance_dir = os.path.join(base_dir, 'instance')
    
    # 確保 instance 目錄存在
    if not os.path.exists(instance_dir):
        os.makedirs(instance_dir)
        
    db_path = os.path.join(instance_dir, 'database.db')
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn
