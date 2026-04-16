from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        # 基本欄位驗證
        if not username or not password:
            flash('帳號與密碼皆為必填欄位！', 'danger')
            return render_template('register.html')
            
        # 檢查該帳號是否已存在
        existing_user = User.get_by_username(username)
        if existing_user:
            flash('該帳號已被人使用，請嘗試其他帳號。', 'danger')
            return render_template('register.html')
            
        # 將密碼進行安全雜湊 (指定使用 pbkdf2:sha256 兼容舊環境)
        password_hash = generate_password_hash(password, method='pbkdf2:sha256')
        new_id = User.create(username, password_hash)
        
        if new_id:
            # 建立成功，清除舊 session、賦予登入資格並重新導向至首頁
            session.clear()
            session['user_id'] = new_id
            session['is_admin'] = 0
            flash(f'註冊成功！歡迎加入讀書筆記本，{username}。', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('註冊時發生系統錯誤，請稍後再試。', 'danger')
            
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        # 透過 DB 取出使用者紀錄
        user = User.get_by_username(username)
        
        # 校驗是否存在以及密碼 hash 是否正確
        if user is None or not check_password_hash(user['password_hash'], password):
            flash('帳號或密碼輸入錯誤，請重試。', 'danger')
            return render_template('login.html')
            
        # 驗證成功，存入 session
        session.clear()
        session['user_id'] = user['id']
        session['is_admin'] = user['is_admin']
        flash(f'歡迎回來，{username}！', 'success')
        return redirect(url_for('main.index'))
        
    return render_template('login.html')

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash('您已成功登出。', 'info')
    return redirect(url_for('main.index'))
