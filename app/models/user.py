import sqlite3
from . import get_db_connection

class User:
    @staticmethod
    def create(username, password_hash, is_admin=0):
        """
        在資料庫中建立新的使用者帳號。

        Args:
            username (str): 使用者名稱（不可重複）。
            password_hash (str): 雜湊處理後的密碼。
            is_admin (int, optional): 身分註記，0為一般用戶，1為管理員。預設為 0。

        Returns:
            int / None: 成功建立後回傳新增使用者的記錄 ID；若發生錯誤（如帳號重複）則回傳 None。
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                '''INSERT INTO users (username, password_hash, is_admin)
                   VALUES (?, ?, ?)''',
                (username, password_hash, is_admin)
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"建立使用者出錯: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_id(user_id):
        """
        依據使用者 ID 搜尋單名使用者的資訊。

        Args:
            user_id (int): 欲查詢的使用者 ID。

        Returns:
            sqlite3.Row / None: 查詢到的資料列代表該使用者；若無則回 None。
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"依 ID 取得使用者出錯: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_username(username):
        """
        依據使用者名稱 (帳號) 搜尋特定使用者。主要用於登入驗證與檢查重複。

        Args:
            username (str): 帳號名稱。

        Returns:
            sqlite3.Row / None: 查詢到的使用者資料列；無則回 None。
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"依 username 取得使用者出錯: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_all():
        """
        取得所有註冊的使用者列表。

        Returns:
            list[sqlite3.Row]: 包含所有用戶的資料列表，發生異常則為空 list。
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users')
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"取得所有使用者出錯: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def update_password(user_id, new_password_hash):
        """
        更新指定使用者的密碼。

        Args:
            user_id (int): 使用者 ID。
            new_password_hash (str): 新的密碼雜湊字串。

        Returns:
            bool: 更新成功回傳 True，發生錯誤或查無此人回傳 False。
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE users SET password_hash = ? WHERE id = ?',
                (new_password_hash, user_id)
            )
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"更新密碼出錯: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def delete(user_id):
        """
        刪除指定使用者及其相關內容配置 (具備 Cascade 以刪除關聯的心得)。

        Args:
            user_id (int): 使用者 ID。

        Returns:
            bool: 成功執行刪除為 True，失敗或異常為 False。
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"刪除使用者出錯: {e}")
            return False
        finally:
            conn.close()
