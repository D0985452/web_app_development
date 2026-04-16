from . import get_db_connection

class Review:
    @staticmethod
    def create(user_id, book_title, book_author, content, rating):
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
        finally:
            conn.close()

    @staticmethod
    def get_by_id(review_id):
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
        finally:
            conn.close()

    @staticmethod
    def get_all():
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            # 撈取列表時順便 JOIN 作者名稱提供頁面渲染
            cursor.execute(
                '''SELECT r.*, u.username as author_name 
                   FROM reviews r 
                   JOIN users u ON r.user_id = u.id 
                   ORDER BY r.created_at DESC'''
            )
            return cursor.fetchall()
        finally:
            conn.close()
            
    @staticmethod
    def search_by_title(keyword):
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
        finally:
            conn.close()

    @staticmethod
    def get_by_user_id(user_id):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                '''SELECT * FROM reviews WHERE user_id = ? ORDER BY created_at DESC''',
                (user_id,)
            )
            return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def update(review_id, book_title, book_author, content, rating):
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
        finally:
            conn.close()

    @staticmethod
    def delete(review_id):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM reviews WHERE id = ?', (review_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()
