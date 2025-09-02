#!/usr/bin/env python3
"""
一口口麻辣串記帳系統 - 快速啟動腳本
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """執行命令並顯示結果"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} 完成")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} 失敗")
        print(f"錯誤: {e.stderr}")
        return False

def check_python_version():
    """檢查 Python 版本"""
    if sys.version_info < (3, 8):
        print("❌ 需要 Python 3.8 或更高版本")
        print(f"當前版本: {sys.version}")
        return False
    print(f"✅ Python 版本: {sys.version.split()[0]}")
    return True

def setup_virtual_environment():
    """建立虛擬環境"""
    venv_path = Path("venv")
    if not venv_path.exists():
        print("\n🔄 建立虛擬環境...")
        if run_command("python -m venv venv", "建立虛擬環境"):
            print("✅ 虛擬環境建立完成")
        else:
            return False
    else:
        print("✅ 虛擬環境已存在")
    return True

def activate_venv_and_install():
    """啟動虛擬環境並安裝依賴"""
    if os.name == 'nt':  # Windows
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
    else:  # Unix/Linux/Mac
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
    
    # 安裝依賴
    if run_command(f"{pip_cmd} install -r requirements.txt", "安裝 Python 依賴"):
        print("✅ 依賴安裝完成")
    else:
        return False
    return True

def setup_database():
    """設定資料庫"""
    print("\n🔄 設定資料庫...")
    
    # 建立 .env 檔案
    env_content = """# 資料庫連線
DB_NAME=onecoco
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=5432

# Django 設定
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# 店面設定
STORE_ID=main_store
"""
    
    with open(".env", "w", encoding="utf-8") as f:
        f.write(env_content)
    
    print("✅ .env 檔案建立完成")
    print("⚠️  請編輯 .env 檔案，設定正確的資料庫連線資訊")
    return True

def run_migrations():
    """執行資料庫遷移"""
    if os.name == 'nt':  # Windows
        python_cmd = "venv\\Scripts\\python"
    else:  # Unix/Linux/Mac
        python_cmd = "venv/bin/python"
    
    if run_command(f"{python_cmd} manage.py makemigrations", "建立資料庫遷移"):
        if run_command(f"{python_cmd} manage.py migrate", "執行資料庫遷移"):
            print("✅ 資料庫遷移完成")
            return True
    
    return False

def create_superuser():
    """建立超級使用者"""
    print("\n🔄 建立超級使用者...")
    print("請輸入以下資訊來建立管理員帳號:")
    
    if os.name == 'nt':  # Windows
        python_cmd = "venv\\Scripts\\python"
    else:  # Unix/Linux/Mac
        python_cmd = "venv/bin/python"
    
    if run_command(f"{python_cmd} manage.py createsuperuser", "建立超級使用者"):
        print("✅ 超級使用者建立完成")
        return True
    
    return False

def start_server():
    """啟動開發伺服器"""
    print("\n🚀 啟動開發伺服器...")
    print("伺服器將在 http://127.0.0.1:8000 啟動")
    print("管理後台: http://127.0.0.1:8000/admin")
    print("按 Ctrl+C 停止伺服器")
    
    if os.name == 'nt':  # Windows
        python_cmd = "venv\\Scripts\\python"
    else:  # Unix/Linux/Mac
        python_cmd = "venv/bin/python"
    
    try:
        subprocess.run(f"{python_cmd} manage.py runserver", shell=True)
    except KeyboardInterrupt:
        print("\n👋 伺服器已停止")

def main():
    """主函數"""
    print("🔥 一口口麻辣串記帳系統")
    print("=" * 50)
    
    # 檢查 Python 版本
    if not check_python_version():
        return
    
    # 建立虛擬環境
    if not setup_virtual_environment():
        return
    
    # 安裝依賴
    if not activate_venv_and_install():
        return
    
    # 設定資料庫
    if not setup_database():
        return
    
    # 執行遷移
    if not run_migrations():
        return
    
    # 建立超級使用者
    if not create_superuser():
        return
    
    # 啟動伺服器
    start_server()

if __name__ == "__main__":
    main()




