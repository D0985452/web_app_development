from flask import Blueprint, render_template, request, redirect, url_for, session, flash

# 建立首頁與搜尋相關的 Blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    [GET] /
    首頁：呼叫 Model 取出最新發布的讀書心得清單，並渲染 index.html 首頁
    """
    pass

@main_bp.route('/search')
def search():
    """
    [GET] /search?q=keyword
    搜尋頁面：接收 query 參數 q 並調用 DB 搜尋符合標題的書籍心得，一樣使用 index.html 渲染內容
    """
    pass
