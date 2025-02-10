#!/bin/bash

# 解析命令行参数
FAST_MODE=false
BACKGROUND=false
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -f|--fast) FAST_MODE=true; shift ;;
        -b|--background) BACKGROUND=true; shift ;;
        *) echo "未知参数: $1"; exit 1 ;;
    esac
done

# 检查虚拟环境是否已激活
if [ -z "$VIRTUAL_ENV" ]; then
    if [ -d "venv" ]; then
        source venv/bin/activate
    else
        echo "虚拟环境不存在，将进行完整安装..."
        FAST_MODE=false
    fi
fi

if [ "$FAST_MODE" = false ]; then
    # 完整安装模式
    # 检查 Python 环境
    if ! command -v python3 &> /dev/null; then
        echo "Python3 未安装，请先安装 Python3"
        exit 1
    fi

    # 检查虚拟环境工具
    if ! command -v python3 -m venv &> /dev/null; then
        echo "Python venv 模块未安装，正在安装..."
        python3 -m pip install --user virtualenv
    fi

    # 创建虚拟环境
    python3 -m venv venv
    source venv/bin/activate

    # 升级 pip
    python -m pip install --upgrade pip

    # 安装核心依赖
    echo "安装核心依赖..."
    pip install python-dotenv streamlit langchain langchain-community langchain-core openai pydantic watchdog

    # 安装其他依赖
    if [ -f "requirements.txt" ]; then
        echo "安装其他依赖..."
        pip install -r requirements.txt
    fi

    # 创建必要的目录和文件
    echo "创建必要的目录和文件..."
    mkdir -p server/config server/models server/services ui/pages ui/components data/messages data/thought_process

    # 创建 __init__.py 文件
    find . -type d -not -path "./venv*" -not -path "./.git*" -exec touch {}/__init__.py \;

    # 检查环境变量文件
    if [ ! -f .env ]; then
        echo "创建 .env 文件..."
        if [ -f .env.example ]; then
            cp .env.example .env
            echo "已从 .env.example 创建 .env 文件，请编辑其中的配置"
        else
            cat > .env << EOL
API_BASE_URL=http://your-api-endpoint
API_KEY=your-api-key
MODEL_NAME=gpt-3.5-turbo
TEMPERATURE=0.7
MAX_TOKENS=1000
EOL
            echo "请编辑 .env 文件，填入正确的 API 配置"
        fi
    fi
else
    # 快速启动模式
    echo "快速启动模式..."
fi

# 启动应用
echo "启动应用..."
# 确保清除任何可能存在的代理设置
unset HTTP_PROXY
unset HTTPS_PROXY

if [ "$BACKGROUND" = true ]; then
    echo "在后台启动应用..."
    nohup python -m streamlit run main.py > streamlit.log 2>&1 &
    PID=$!
    echo $PID > .streamlit.pid
    echo "应用已在后台启动，PID: $PID"
    echo "查看日志: tail -f streamlit.log"
    echo "停止应用: kill $(cat .streamlit.pid)"
else
    python -m streamlit run main.py
fi 