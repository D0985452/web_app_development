from flask import Blueprint, render_template, request, redirect, url_for, session, flash

# 建立文章管理的 Blueprint，URL 統一掛在 /review 下
review_bp = Blueprint('review', __name__, url_prefix='/review')

@review_bp.route('/create', methods=['GET', 'POST'])
def create():
    """
    [GET] /review/create: 渲染 review_form.html (空白表單)。需要確認已登入。
    [POST] /review/create: 接收書名、作者、內文與評分並存入 DB。成功後導回明細頁。
    """
    pass

@review_bp.route('/<int:id>')
def detail(id):
    """
    [GET] /review/<id>: 使用 id 查詢單篇心得，並渲染 review_detail.html。若查無資料回傳 404。
    """
    pass

@review_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    """
    [GET] /review/<id>/edit: 檢查使用者身份與作者相符後，帶入舊資料渲染 review_form.html。
    [POST] /review/<id>/edit: 接收更改的表單內容，更新 DB，然後導向該文章詳情頁。
    """
    pass

@review_bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    [POST] /review/<id>/delete: 檢查是否為對應文章作者或管理員，刪除此文章，最後重導回首頁。
    """
    pass
