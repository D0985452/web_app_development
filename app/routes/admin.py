from flask import Blueprint, render_template, request, redirect, url_for, session, flash

# 建立管理員後台的 Blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/reviews')
def reviews_list():
    """
    [GET] /admin/reviews:
    管理員專屬後台，需要檢查 session 中 is_admin 是否為 1 才能進入。
    渲染 admin.html 列出所有用戶文章。
    """
    pass
