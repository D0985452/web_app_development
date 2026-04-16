import sqlite3
from . import get_db_connection

class Review:
    @staticmethod
    def create(user_id, book_title, book_author, content, rating):
        """
        新增一篇讀書心得。

        Args:
            user_id (int): 發表此心得的使用者 ID。
            book_title (str): 書籍名稱。
            book_author (str): 書籍作者。
            content (str): 心得內文。
            rating (int): 對書籍的評分 (如 1-5)。

        Returns:
            int / None: 成功新增後回傳文章 ID；若失敗回傳 None。
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                '''INSERT INTO reviews (user_id, book_title, book_author, content, rating)
                   VALUES (?, ?, ?, ?, ?)''',
                (user_id, book_title, book_author, content, rating)
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"新增心得發生錯誤: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_id(review_id):
        """
        依心得文章 ID 撈取單篇文章，並透過 JOIN 一併取得作者名稱以便顯示。

        Args:
            review_id (int): 心得文章 ID。

        Returns:
            sqlite3.Row / None: 單篇文章關聯結果；若查無此文則回傳 None。
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                '''SELECT r.*, u.username as author_name 
                   FROM reviews r 
                   JOIN users u ON r.user_id = u.id 
                   WHERE r.id = ?''', 
                (review_id,)
            )
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"取得單篇心得時出錯: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_all():
        """
        取得所有心得的列表，依照最新建檔時間排序，並 JOIN 取得每篇的發布者名稱。主要用於首頁或管理背景展示。

        Returns:
            list[sqlite3.Row]: 心得資料列串列，若異常為空 list。
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                '''SELECT r.*, u.username as author_name 
                   FROM reviews r 
                   JOIN users u ON r.user_id = u.id 
                   ORDER BY r.created_at DESC'''
            )
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"取得心得清單出錯: {e}")
            return []
        finally:
            conn.close()
            
    @staticmethod
    def search_by_title(keyword):
        """
        根據書名字進行模糊搜尋。

        Args:
            keyword (str): 要被搜尋的書名關鍵字。

        Returns:
            list[sqlite3.Row]: 符合關鍵字之所有心得聯集結果。
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            search_pattern = f'%{keyword}%'
            cursor.execute(
                '''SELECT r.*, u.username as author_name 
                   FROM reviews r 
                   JOIN users u ON r.user_id = u.id 
                   WHERE r.book_title LIKE ?
                   ORDER BY r.created_at DESC''',
                (search_pattern,)
            )
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"搜尋文章時發生錯誤: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def get_by_user_id(user_id):
        """
        找尋某個特定使用者所發布的所有讀書心得。

        Args:
            user_id (int): 使用者 ID。

        Returns:
            list[sqlite3.Row]: 該使用者寫過的所有文章串列。
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                '''SELECT * FROM reviews WHERE user_id = ? ORDER BY created_at DESC''',
                (user_id,)
            )
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"依使用者找心得發生錯誤: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def update(review_id, book_title, book_author, content, rating):
        """
        更新特定讀書心得的資訊。

        Args:
            review_id (int): 心得 ID。
            book_title (str): 新書名。
            book_author (str): 新作者。
            content (str): 新內容。
            rating (int): 新評分。

        Returns:
            bool: 更新成功回傳 True，否則為 False。
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                '''UPDATE reviews 
                   SET book_title = ?, book_author = ?, content = ?, rating = ?
                   WHERE id = ?''',
                (book_title, book_author, content, rating, review_id)
            )
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"更新心得發生錯誤: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def delete(review_id):
        """
        刪除特定讀書心得文章。可以被原作者或管理員叫用。

        Args:
            review_id (int): 要刪除的文章 ID。

        Returns:
            bool: 成功執行則回傳 True。
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM reviews WHERE id = ?', (review_id,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"刪除心得時發生異常: {e}")
            return False
        finally:
            conn.close()
