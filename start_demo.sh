#!/bin/bash
# 启动演示脚本

echo "🚀 启动AI健康小程序演示..."
echo "================================"

# 检查必要的依赖
echo "📋 检查环境依赖..."

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装"
    exit 1
fi

# 检查Node.js
if ! command -v npm &> /dev/null; then
    echo "❌ Node.js/npm 未安装"
    exit 1
fi

echo "✅ 环境依赖检查通过"

# 启动后端
echo ""
echo "🔧 启动后端服务..."
cd backend

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "⚠️ 虚拟环境不存在，创建中..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo "📦 安装后端依赖..."
pip install -r requirements.txt

# 检查环境变量
if [ ! -f ".env" ]; then
    echo "⚠️ .env文件不存在，请确保已配置OpenRouter API密钥"
fi

# 启动后端服务
echo "🟢 启动后端服务 (端口 8000)..."
python main.py &
BACKEND_PID=$!

# 等待后端启动
sleep 3

# 启动前端
echo ""
echo "🎨 启动前端服务..."
cd ../frontend

# 安装依赖
echo "📦 安装前端依赖..."
npm install

# 启动前端服务
echo "🟢 启动前端服务 (端口 5173)..."
npm run dev &
FRONTEND_PID=$!

echo ""
echo "🎉 演示启动成功！"
echo "================================"
echo "📱 前端访问地址: http://localhost:5173"
echo "🔧 后端API地址: http://localhost:8000"
echo "📚 API文档: http://localhost:8000/docs"
echo ""
echo "按 Ctrl+C 停止所有服务"

# 等待中断信号
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait