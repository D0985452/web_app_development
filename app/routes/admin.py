from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort
from app.models.review import Review

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/reviews')
def reviews_list():
    """管理員後台首頁 - 取出全部文章以供檢查，需阻擋沒有管理員權限者。"""
    if session.get('is_admin') != 1:
        abort(403) # 丟出 HTTP 403 Forbidden 狀態碼
        
    reviews = Review.get_all()
    return render_template('admin.html', reviews=reviews)
