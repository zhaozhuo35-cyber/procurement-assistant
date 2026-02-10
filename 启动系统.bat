@echo off
chcp 65001 >nul
echo ========================================
echo 智能采购助手系统 - 快速启动
echo ========================================
echo.

echo [1/3] 检查Python环境...
python --version
if errorlevel 1 (
    echo 错误：未找到Python，请先安装Python 3.8+
    pause
    exit
)

echo.
echo [2/3] 安装依赖包...
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
if errorlevel 1 (
    echo 警告：部分依赖安装失败，尝试继续...
)

echo.
echo [3/3] 启动系统...
echo 系统将在浏览器中自动打开
echo 访问地址: http://localhost:8501
echo.
echo 按 Ctrl+C 可停止系统
echo ========================================
echo.

streamlit run app.py

pause
