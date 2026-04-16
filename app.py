from dotenv import load_dotenv
import os

# 嘗試載入 .env 檔案
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from app import create_app

app = create_app()

if __name__ == '__main__':
    # 預設以 5000 port 與 debug 模式執行
    app.run(debug=True, port=5000)
