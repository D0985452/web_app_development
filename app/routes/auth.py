from flask import Blueprint, render_template, request, redirect, url_for, session, flash

# 建立會員認證的 Blueprint，URL 統一掛在 /auth 下
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    [GET] /auth/register: 顯示會員註冊表單 register.html
    [POST] /auth/register: 接收 username 與 password 參數，驗證合法性後新建帳號。
                           成功自動登入並切換到首頁。
    """
    pass

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    [GET] /auth/login: 顯示登入表單 login.html
    [POST] /auth/login: 驗證帳密。成功後建立 Session 並切換到首頁。錯誤則給予提示。
    """
    pass

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """
    [POST] /auth/logout: 清除當前的登入 Session。重導向至首頁。
    """
    pass
