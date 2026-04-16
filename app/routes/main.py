from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.review import Review

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """首頁：顯示所有讀書心得。"""
    reviews = Review.get_all()
    return render_template('index.html', reviews=reviews)

@main_bp.route('/search')
def search():
    """搜尋頁面：根據 query q 查詢書籍名稱。"""
    query = request.args.get('q', '').strip()
    if query:
        reviews = Review.search_by_title(query)
    else:
        reviews = Review.get_all()
    return render_template('index.html', reviews=reviews, query=query)
