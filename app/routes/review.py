from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort
from functools import wraps
from app.models.review import Review

review_bp = Blueprint('review', __name__, url_prefix='/review')

def login_required(f):
    """自訂義裝飾器：阻擋未登入的請求並重導回登入頁面。"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('請先登入會員後再進行操作！', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@review_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        book_title = request.form.get('book_title', '').strip()
        book_author = request.form.get('book_author', '').strip()
        content = request.form.get('content', '').strip()
        try:
            rating = int(request.form.get('rating', 0))
        except ValueError:
            rating = 0
            
        if not book_title or not content:
            flash('書名與心得內文皆不可為空白。', 'danger')
            return render_template('review_form.html', action='create')
            
        if rating < 1 or rating > 5:
            flash('請輸入 1 到 5 之間的評分數值。', 'warning')
            return render_template('review_form.html', action='create')
            
        new_id = Review.create(session['user_id'], book_title, book_author, content, rating)
        
        if new_id:
            flash('太棒了！您的讀書心得已經順利發布！', 'success')
            return redirect(url_for('review.detail', id=new_id))
        else:
            flash('系統發生錯誤導致發布失敗，請稍後重試。', 'danger')
            
    # GET method
    return render_template('review_form.html', action='create')

@review_bp.route('/<int:id>')
def detail(id):
    review = Review.get_by_id(id)
    if not review:
        abort(404)
    return render_template('review_detail.html', review=review)

@review_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    review = Review.get_by_id(id)
    if not review:
        abort(404)
        
    # 需要是該篇文章原作者，或是管理員，才可以有編輯權限
    if review['user_id'] != session['user_id'] and session.get('is_admin') != 1:
        flash('抱歉，您沒有修改這篇文章的權限。', 'danger')
        return redirect(url_for('review.detail', id=id))
        
    if request.method == 'POST':
        book_title = request.form.get('book_title', '').strip()
        book_author = request.form.get('book_author', '').strip()
        content = request.form.get('content', '').strip()
        try:
            rating = int(request.form.get('rating', 0))
        except ValueError:
            rating = 0
            
        if not book_title or not content:
            flash('書名與心得內文皆不可為空白。', 'danger')
            return render_template('review_form.html', action='edit', review=review)
            
        if rating < 1 or rating > 5:
            flash('請輸入 1 到 5 之間的評分數值。', 'warning')
            return render_template('review_form.html', action='edit', review=review)
            
        success = Review.update(id, book_title, book_author, content, rating)
        if success:
            flash('文章修改已儲存！', 'success')
            return redirect(url_for('review.detail', id=id))
        else:
            flash('存檔失敗，請確認資料是否正確。', 'danger')
            
    # GET method 帶入原始資料以便編輯
    return render_template('review_form.html', action='edit', review=review)

@review_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    review = Review.get_by_id(id)
    if not review:
        abort(404)
        
    if review['user_id'] != session['user_id'] and session.get('is_admin') != 1:
        flash('抱歉，您無法刪除不屬於您的文章。', 'danger')
        return redirect(url_for('main.index'))
        
    if Review.delete(id):
        flash('文章已經成功刪除了。', 'success')
    else:
        flash('刪除過程中發生未知錯誤。', 'danger')
        
    return redirect(url_for('main.index'))
